from django.conf.urls import patterns, include, url

from .views import blogviews

#==============================================================================#
IDENT = r'[\w\d\-_]+'
urlparams = {
    'BLOGID': IDENT,
}

def sub(urlfmt):
    return urlfmt.format(**urlparams)


#==============================================================================#
urlpatterns = patterns('',
    (sub(r'^blogs/(?P<blogid>{BLOGID})/$'), blogviews.BlogMainView.as_view(), {}, 'blog-main'),
)

#==============================================================================#
