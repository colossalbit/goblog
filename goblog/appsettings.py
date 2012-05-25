from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

## GOBLOG_TAGSPACE_DEFAULT = getattr(settings, 'GOBLOG_TAGSPACE_DEFAULT', 'shared')
## # other values: 'shared', 'perblog', 'none'

GOBLOG_DEFAULT_BLOG = getattr(settings, 'GOBLOG_DEFAULT_BLOG', None)

_DEFAULT_ARTICLE_COMPILERS = {
    u'basic':        u'goblog.core.articlecompilers.BasicArticleCompiler',
    u'cleanhtml':    u'goblog.core.articlecompilers.CleanHtmlArticleCompiler',
    u'nohtml':       u'goblog.core.articlecompilers.NoHtmlArticleCompiler',
}
def _get_article_compiler_default(compilers):
    for name in ['cleanhtml','nohtml']:
        if name in compilers:
            return name
    # arbitrary compiler
    return compilers.keys[0]

# GOBLOG_ARTICLE_COMPILERS 
GOBLOG_ARTICLE_COMPILERS = getattr(settings, 'GOBLOG_ARTICLE_COMPILERS', _DEFAULT_ARTICLE_COMPILERS)
if not isinstance(GOBLOG_ARTICLE_COMPILERS, dict):
    raise ImproperlyConfigured("'GOBLOG_ARTICLE_COMPILERS' must be a dict.")
if len(GOBLOG_ARTICLE_COMPILERS) == 0:
    raise ImproperlyConfigured("'GOBLOG_ARTICLE_COMPILERS' must not be empty.")

# GOBLOG_ARTICLE_COMPILER_DEFAULT 
GOBLOG_ARTICLE_COMPILER_DEFAULT = getattr(settings, 'GOBLOG_ARTICLE_COMPILER_DEFAULT', None)
if not GOBLOG_ARTICLE_COMPILER_DEFAULT:
    GOBLOG_ARTICLE_COMPILER_DEFAULT = _get_article_compiler_default(GOBLOG_ARTICLE_COMPILERS)

ARTICLE_COMPILER_CHOICES = tuple((k,k) for k in sorted(GOBLOG_ARTICLE_COMPILERS.keys()))

BLOGSPACE_NAME_MAXLEN = 100
BLOG_NAME_MAXLEN = 100
ARTICLE_NAME_MAXLEN = 32  # UUID
TAG_NAME_MAXLEN = 100
ARTICLE_COMPILER_MAXLEN = 255
##ARTICLE_COMPILER_DEFAULT = u'nohtml'

