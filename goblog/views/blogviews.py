from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.utils import timezone as djtimezone
from django.core.urlresolvers import reverse as urlreverse
from django.contrib.auth.models import User

from django.db import connections
from django.db.models import Count, DateTimeField

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
        
    def get_articles_queryset(self):
        # articles must be published
        # published date must be at or before now
        now = self.now or djtimezone.now()
        qs = models.Article.objects.exclude(published=None).exclude(published__gt=now)
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
        qs = qs.extra(select={'published': connections[models.Article.objects.db].ops.date_trunc_sql('month', 'published')})
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
            context['blog'] = models.Blog.objects.get(
                                                    name=self.kwargs['blogid'])
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
    
    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['blog'] = context['article'].blog
        return context
    

#==============================================================================#
class ArticleCreateView(FormView):
    form_class = forms.ArticleCreateForm
    template_name = 'goblog/article_create.html'
    
    def get_blogid(self):
        return self.kwargs['blogid']
        
    def get_blog(self):
        if not hasattr(self, '_blog'):
            self._blog = models.Blog.objects.get(name=self.get_blogid())
        return self._blog
    
    def get_authorid(self):
        return self.request.user.id
    
    def get_author(self):
        if not hasattr(self, '_author'):
            self._author = User.objects.get(id=self.get_authorid())
        return self._author
    
    def get_success_url(self):
        # TODO: make success URL redirect to article
        return urlreverse('blog-main', kwargs={'blogid': self.get_blogid()})
        
    def show_preview(self):
        return self.request.POST.get('submit', None) == 'Preview'
        
    def get_context_data(self, **kwargs):
        context = super(ArticleCreateView, self).get_context_data(**kwargs)
        context['blog'] = self.get_blog()
        return context
        
    def create_article(self, form):
        import uuid
        blog = self.get_blog()
        articleargs = {
            'id': uuid.uuid4().hex,
            'blog': blog,
            'author': self.get_author(),
            'title': form.cleaned_data['title'],
            'compiler_name': form.cleaned_data['compiler_name'],
        }
        article = models.Article(**articleargs)
        article.save()
        return article
        
    def create_article_content(self, form, article):
        contentargs = {
            'article': article,
            'raw': form.cleaned_data['text'],
            'full': form.article_full,
            'brief': form.article_brief,
        }
        content = models.ArticleContent(**contentargs)
        content.save()
        return content
        
    def form_valid(self, form):
        # TODO: allow preview before saving
        article = self.create_article(form)
        content = self.create_article_content(form, article)
        return super(ArticleCreateView, self).form_valid(form)
        
    def form_valid(self, form):
        if self.show_preview():
            context = self.get_context_data(form=form, 
                                            preview_content=form.article_full)
            return self.render_to_response(context)
        else:
            article = self.create_article(form)
            content = self.create_article_content(form, article)
            return super(ArticleCreateView, self).form_valid(form)


class ArticleEditView(FormView):
    form_class = forms.ArticleEditForm
    template_name = 'goblog/article_edit.html'
    
    def get_blogid(self):
        return self.kwargs['blogid']
        
    def get_blog(self):
        if not hasattr(self, '_blog'):
            self._blog = models.Blog.objects.get(name=self.get_blogid())
        return self._blog
    
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
            self._article = models.Article.objects.select_related('content').get(id=self.get_articleid())
        return self._article
        
    def get_article_content(self):
        return self.get_article().content
    
    def get_success_url(self):
        # TODO: make success URL redirect to article
        return urlreverse('blog-main', kwargs={'blogid': self.get_blogid()})
        
    def show_preview(self):
        return self.request.POST.get('submit', None) == 'Preview'
        
    def get_context_data(self, **kwargs):
        context = super(ArticleEditView, self).get_context_data(**kwargs)
        context['blog'] = self.get_blog()
        return context
        
    def update_article(self, form):
        article = self.get_article()
        article.title = form.cleaned_data['title']
        article.compiler_name = form.cleaned_data['compiler_name']
        article.save()
        self._article = article
        return article
        
    def update_article_content(self, form):
        content = self.get_article_content()
        content.raw = form.cleaned_data['text']
        content.full = form.article_full
        content.brief = form.article_brief
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
        
    def form_valid(self, form):
        # TODO: allow preview before saving
        article = self.update_article(form)
        content = self.update_article_content(form)
        edit = self.create_article_edit(form, article)
        return super(ArticleEditView, self).form_valid(form)
        
    def form_valid(self, form):
        if self.show_preview():
            context = self.get_context_data(form=form, 
                                            preview_content=form.article_full)
            return self.render_to_response(context)
        else:
            article = self.update_article(form)
            content = self.update_article_content(form)
            edit = self.create_article_edit(form, article)
            return super(ArticleEditView, self).form_valid(form)

#==============================================================================#
