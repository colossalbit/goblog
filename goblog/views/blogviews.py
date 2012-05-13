from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.utils import timezone as djtimezone
from django.core.urlresolvers import reverse as urlreverse
from django.contrib.auth.models import User

from .. import models, forms

#==============================================================================#
class ArticleListMixin(object):
    model = models.Article
    context_object_name = 'articles'
    
    now = None
    blogid = None
    authorid = None
    
    def get_blogid(self):
        return self.blogid
    
    def get_authorid(self):
        return self.authorid

    def get_queryset(self):
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
        
        # As of Django 1.4, a bug prevents us from using select_related() and 
        # defer() in queries on the reverse OneToOne relationships.  Once 
        # fixed, it would probably be a good idea to do something like the 
        # following to get the article contents:
        ##qs = qs.select_related('content').defer('content__raw')
        qs = qs.select_related('content')
        return qs
        
        
#==============================================================================#
class BlogView(ArticleListMixin, ListView):
    template_name = 'goblog/blogmain.html'
    
    def get_blogid(self):
        return self.kwargs['blogid']
    
    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        try:
            context['blog'] = models.Blog.objects.get(
                                                    name=self.kwargs['blogid'])
        except ObjectDoesNotExist:
            raise Http404('Blog not found.')
        return context
        

class ArticleView(DetailView):
    model = models.Article
    slug_field = 'id'
    slug_url_kwarg = 'articleid'
    context_object_name = 'article'
    template_name = 'goblog/article.html'
    

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
        return urlreverse('blog-main', kwargs={'blogid': self.get_blogid()})
        
    def get_context_data(self, **kwargs):
        context = super(ArticleCreateView, self).get_context_data(**kwargs)
        context['blog'] = self.get_blog()
        return context
        
    def form_valid(self, form):
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
        contentargs = {
            'article': article,
            'raw': form.cleaned_data['text'],
            'full': form.article_full,
            'brief': form.article_brief,
        }
        content = models.ArticleContent(**contentargs)
        content.save()
        return super(ArticleCreateView, self).form_valid(form)

#==============================================================================#
