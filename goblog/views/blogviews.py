from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import Http404, HttpResponseForbidden
from django.utils import timezone as djtimezone
from django.core.urlresolvers import reverse as urlreverse
from django.contrib.auth.models import User
# views:
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView

from django.db import connections
from django.db.models import Count
from django.conf import settings

from .. import models, forms

#==============================================================================#
class GoBlogMixin(object):
    now = None  # facilitates testing without regard to the current date
    blogid = None
    authorid = None
    
    recent_articles_size = 5
    
    def get_blogid(self):
        return self.blogid
    
    def get_authorid(self):
        return self.authorid
        
    def get_now(self):
        return self.now or djtimezone.now()
        
    def get_articles_queryset(self):
        # articles must be published
        # published date must be at or before now
        now = self.get_now()
        qs = models.Article.objects.exclude(published=None)
        qs = qs.exclude(published__gt=now)
        # articles must be part of the chosen blog
        blogid = self.get_blogid()
        if blogid:
            qs = qs.filter(blog=blogid)
        # articles must have selected author
        authorid = self.get_authorid()
        if authorid:
            qs = qs.filter(author=authorid)
        # articles must be sorted by published date
        qs = qs.order_by('-published')
        # TODO: articles must have chosen tag(s)
        # TODO: articles must match search criteria
        
        return qs
    
    def get_archives_list(self):
        qs = self.get_articles_queryset()
        conn = connections[models.Article.objects.db]
        qs = qs.extra(select={'published': 
                              conn.ops.date_trunc_sql('month', 'published')})
        qs = qs.values('published')
        qs = qs.annotate(dcount=Count('published'))
        # get the 'published' Field instance
        pfield = models.Article._meta.get_field('published')
        # Wrapping in generator function allows the results to be iterated over 
        # multiple times
        def _iter():
            for obj in qs:
                yield {
                    # convert from string to datetime.datetime object
                    'date':  pfield.to_python(obj['published']), 
                    'count': obj['dcount']
                }
        return _iter
        
    def get_recent_articles_list(self):
        qs = self.get_articles_queryset()[:self.recent_articles_size]
        return qs
        
    def get_login_redirect_url(self):
        return self.request.path
        
    def get_logout_redirect_url(self):
        return self.request.path
        
    def get_context_data(self, **kwargs):
        supercls = super(GoBlogMixin, self)
        if hasattr(supercls, 'get_context_data'):
            context = supercls.get_context_data(**kwargs)
        else:
            context = kwargs
        context['LOGIN_URL'] = settings.LOGIN_URL
        context['LOGOUT_URL'] = settings.LOGOUT_URL
        context['LOGIN_REDIRECT_URL'] = self.get_login_redirect_url()
        context['LOGOUT_REDIRECT_URL'] = self.get_logout_redirect_url()
        return context
        
        
#==============================================================================#
class BlogView(GoBlogMixin, ListView):
    model = models.Article
    context_object_name = 'articles'
    template_name = 'goblog/blogmain.html'
    
    def get_blogid(self):
        return self.kwargs['blogid']
        
    def get_queryset(self):
        qs = self.get_articles_queryset()
        
        # As of Django 1.4, a bug prevents us from using select_related() and 
        # defer() in queries on the reverse OneToOne relationships.  Once 
        # fixed, it would probably be a good idea to do something like the 
        # following to get the article contents:
        ##qs = qs.select_related('content').defer('content__raw')
        qs = qs.select_related('content')
        return qs
    
    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        try:
            context['blog'] = models.Blog.objects.get(name=self.get_blogid())
        except ObjectDoesNotExist:
            raise Http404('Blog not found.')
        context['archives'] = self.get_archives_list()
        context['recent_articles'] = self.get_recent_articles_list()
        return context
        

class ArticleView(GoBlogMixin, DetailView):
    model = models.Article
    slug_field = 'id'
    slug_url_kwarg = 'articleid'
    context_object_name = 'article'
    template_name = 'goblog/article.html'
    
    def get_blogid(self):
        return self.kwargs['blogid']
        
    def get_object(self, queryset=None):
        article = super(ArticleView, self).get_object(queryset=queryset)
        now = self.get_now()
        # Permissions required to see unpublished articles
        if article.published is None or now < article.published:
            if not article.user_can_see_unpublished_article(self.request.user):
                raise Http404('Article not found.')  # Should this be 403?
        return article
    
    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        try:
            context['blog'] = models.Blog.objects.get(name=self.get_blogid())
        except ObjectDoesNotExist:
            raise Http404('Blog not found.')
        return context
    

#==============================================================================#
class ArticleFormView(GoBlogMixin, FormView):
        
    def get_blogid(self):
        return self.kwargs['blogid']
        
    def get_blog(self):
        if not hasattr(self, '_blog'):
            self._blog = models.Blog.objects.get(name=self.get_blogid())
        return self._blog
    
    def get_success_url(self):
        # TODO: make success URL redirect to article
        return urlreverse('goblog-blog-main', 
                          kwargs={'blogid': self.get_blogid()})
        
    def get_logout_redirect_url(self):
        return self.get_blog().get_absolute_url()
        
    def show_preview(self):
        return self.request.POST.get('submit', None) == 'Preview'
        
    def get_context_data(self, **kwargs):
        context = super(ArticleFormView, self).get_context_data(**kwargs)
        context['blog'] = self.get_blog()
        return context
            
    def get(self, request, *args, **kwargs):
        if not self.validate_user_permissions(request):
            return HttpResponseForbidden()
        else:
            return super(ArticleFormView, self).get(request, *args, **kwargs)
            
    def post(self, request, *args, **kwargs):
        if not self.validate_user_permissions(request):
            raise HttpResponseForbidden()
        else:
            return super(ArticleFormView, self).post(request, *args, **kwargs)


class ArticleCreateView(ArticleFormView):
    form_class = forms.ArticleCreateForm
    template_name = 'goblog/article_create.html'
    
    def get_authorid(self):
        return self.request.user.id
    
    def get_author(self):
        if not hasattr(self, '_author'):
            self._author = User.objects.get(id=self.get_authorid())
        return self._author
        
    def create_article(self, form):
        import uuid
        blog = self.get_blog()
        articleargs = {
            'id': uuid.uuid4().hex,
            'blog': blog,
            'author': self.get_author(),
            'title': form.cleaned_data['title'],
            'compiler_name': form.cleaned_data['compiler_name'],
            'published': form.cleaned_data['published'],
        }
        article = models.Article(**articleargs)
        article.save()
        return article
        
    def create_article_content(self, form, article):
        contentargs = {
            'article': article,
            'raw': form.cleaned_data['text'],
            'text_start': form.article_start,
            'text_end': form.article_end,
        }
        content = models.ArticleContent(**contentargs)
        content.save()
        return content
        
    def validate_user_permissions(self, request):
        try:
            blog = self.get_blog()
        except ObjectDoesNotExist:
            raise Http404('Blog not found.')
        return blog.user_can_create_article(request.user)
        
    def form_valid(self, form):
        if self.show_preview():
            context = self.get_context_data(form=form, 
                                            preview_start=form.article_start,
                                            preview_end=form.article_end)
            return self.render_to_response(context)
        else:
            article = self.create_article(form)
            content = self.create_article_content(form, article)
            return super(ArticleCreateView, self).form_valid(form)


class ArticleEditView(ArticleFormView):
    form_class = forms.ArticleEditForm
    template_name = 'goblog/article_edit.html'
    
    def get_editorid(self):
        return self.request.user.id
    
    def get_editor(self):
        if not hasattr(self, '_editor'):
            self._editor = User.objects.get(id=self.get_editorid())
        return self._editor
    
    def get_articleid(self):
        return self.kwargs['articleid']
    
    def get_article(self):
        if not hasattr(self, '_article'):
            qs = models.Article.objects.select_related('content')
            self._article = qs.get(id=self.get_articleid())
        return self._article
        
    def get_article_content(self):
        return self.get_article().content
        
    def update_article(self, form):
        article = self.get_article()
        article.title = form.cleaned_data['title']
        article.compiler_name = form.cleaned_data['compiler_name']
        article.published = form.cleaned_data['published']
        article.save()
        self._article = article
        return article
        
    def update_article_content(self, form):
        content = self.get_article_content()
        content.raw = form.cleaned_data['text']
        content.text_start = form.article_start
        content.text_end = form.article_end
        content.save()
        return content
        
    def create_article_edit(self, form, article):
        kwargs = {
            'article': article,
            'editor': self.get_editor(),
        }
        edit = models.ArticleEdit(**kwargs)
        edit.save()
        return edit
        
    def get_context_data(self, **kwargs):
        context = super(ArticleEditView, self).get_context_data(**kwargs)
        context['article'] = self.get_article()
        return context
        
    def get_form_kwargs(self):
        kwargs = super(ArticleEditView, self).get_form_kwargs()
        if self.request.method in ('GET',):
            article = self.get_article()
            # 'published' can be None
            if article.published:
                tz = djtimezone.get_current_timezone()
                published = article.published.astimezone(tz)
                published_date = published.date()
                published_time = published.timetz()
            else:
                published_date = None
                published_time = None
            data = {
                'title': article.title,
                'published_0': published_date, 
                'published_1': published_time,
                'compiler_name': article.compiler_name,
                'text': article.content.raw,
            }
            kwargs.update({
                'data': data,
            })
        return kwargs
        
    def validate_user_permissions(self, request):
        try:
            article = self.get_article()
        except ObjectDoesNotExist:
            raise Http404('Article not found.')
        return article.user_can_edit_article(request.user)
        
    def form_valid(self, form):
        if self.show_preview():
            context = self.get_context_data(form=form, 
                                            preview_start=form.article_start,
                                            preview_end=form.article_end)
            return self.render_to_response(context)
        else:
            article = self.update_article(form)
            content = self.update_article_content(form)
            edit = self.create_article_edit(form, article)
            return super(ArticleEditView, self).form_valid(form)


#==============================================================================#
def i18n_javascript(request):
    # taken from django.contrib.admin.sites.AdminSite.i18n_javascript
    if settings.USE_I18N:
        from django.views.i18n import javascript_catalog
    else:
        from django.views.i18n import null_javascript_catalog as javascript_catalog
    return javascript_catalog(request, packages=['django.conf', 'django.contrib.admin'])

#==============================================================================#



