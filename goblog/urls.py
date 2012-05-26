from django.conf.urls import patterns, include, url

from .views import blogviews

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
    # TODO: blog/
    # TODO: blog/new_article/
    # TODO: blog/archive/YYYY/MM/
    # TODO: blog/articles/
    # TODO: blog/articles/ARTICLEID/
    # TODO: blog/articles/ARTICLEID/edit/
    
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
