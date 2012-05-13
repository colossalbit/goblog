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
    # blogs/BLOGID/
    (sub(r'^blogs/(?P<blogid>{BLOGID})/$'), blogviews.BlogView.as_view(), {}, 'blog-main'),
    # blogs/BLOGID/articles/ARTICLEID/
    (sub(r'^blogs/(?P<blogid>{BLOGID})/articles/(?P<articleid>{ARTICLEID})/$'), blogviews.ArticleView.as_view(), {}, 'article-view'),
    # blogs/BLOGID/new_article/
    (sub(r'^blogs/(?P<blogid>{BLOGID})/new_article/$'), blogviews.ArticleCreateView.as_view(), {}, 'article-create'),
)

#==============================================================================#
