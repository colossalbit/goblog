from django.conf.urls import patterns, include, url

from .views import blogviews
##from .appsettings import DEFAULT_BLOG_MARKER

#==============================================================================#
IDENT = r'[\w\d\-_]+'
urlparams = {
    'BLOGID': IDENT,
    'ARTICLEID': IDENT,
}

def sub(urlfmt):
    return urlfmt.format(**urlparams)

#==============================================================================#
urlpatterns = patterns('',
    ##(sub(r'^blogs/(?P<blogid>{BLOGID})/$'), blogviews.BlogMainView.as_view(), {}, 'blog-main'),
    # blog/
    (sub(r'^blog/$'), blogviews.BlogView.as_view(), {'default_blog': True}, 'goblog-default-blog-main'),
    # blog/new_article/
    (sub(r'^blog/new_article/$'), blogviews.ArticleCreateView.as_view(), {'default_blog': True}, 'goblog-default-article-create'),
    # TODO: blog/archive/YYYY/MM/
    # blog/articles/
    (sub(r'^blog/articles/$'), blogviews.ArticlesView.as_view(), {'default_blog': True}, 'goblog-default-articles-view'),
    # blog/articles/ARTICLEID/
    (sub(r'^blog/articles/(?P<articleid>{ARTICLEID})/$'), blogviews.ArticleView.as_view(), {'default_blog': True}, 'goblog-default-article-view'),
    # blog/articles/ARTICLEID/edit/
    (sub(r'^blog/articles/(?P<articleid>{ARTICLEID})/edit/$'), blogviews.ArticleEditView.as_view(), {'default_blog': True}, 'goblog-default-article-edit'),
    
    # blogs/BLOGID/
    (sub(r'^blogs/(?P<blogid>{BLOGID})/$'), blogviews.BlogView.as_view(), {}, 'goblog-blog-main'),
    
    # blogs/BLOGID/new_article/
    (sub(r'^blogs/(?P<blogid>{BLOGID})/new_article/$'), blogviews.ArticleCreateView.as_view(), {}, 'goblog-article-create'),
    
    # TODO: blogs/BLOGID/archive/YYYY/MM/
    
    # blogs/BLOGID/articles/
    (sub(r'^blogs/(?P<blogid>{BLOGID})/articles/$'), blogviews.ArticlesView.as_view(), {}, 'goblog-articles-view'),
    
    # blogs/BLOGID/articles/ARTICLEID/
    (sub(r'^blogs/(?P<blogid>{BLOGID})/articles/(?P<articleid>{ARTICLEID})/$'), blogviews.ArticleView.as_view(), {}, 'goblog-article-view'),
    
    # blogs/BLOGID/articles/ARTICLEID/edit/
    (sub(r'^blogs/(?P<blogid>{BLOGID})/articles/(?P<articleid>{ARTICLEID})/edit/$'), blogviews.ArticleEditView.as_view(), {}, 'goblog-article-edit'),
    
    (r'^blogutil/jsi18n/$', blogviews.i18n_javascript, {}, 'goblog-i18n-javascript'),
)

#==============================================================================#
