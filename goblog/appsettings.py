from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import signals as test_signals


#==============================================================================#
_DEFAULT_ARTICLE_COMPILERS = {
    u'basic':        u'goblog.core.articlecompilers.BasicArticleCompiler',
    u'cleanhtml':    u'goblog.core.articlecompilers.CleanHtmlArticleCompiler',
    u'nohtml':       u'goblog.core.articlecompilers.NoHtmlArticleCompiler',
}

def _get_article_compiler_default(compilers):
    # 'compilers' must be a non-empty dict
    for name in ['cleanhtml','nohtml']:
        if name in compilers:
            return name
    # arbitrary compiler
    return compilers.keys[0]

#==============================================================================#
def load_settings():
    # GOBLOG_DEFAULT_BLOG 
    GOBLOG_DEFAULT_BLOG = getattr(settings, 'GOBLOG_DEFAULT_BLOG', None)

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
    
    # GOBLOG_DEFAULT_THEME
    GOBLOG_DEFAULT_THEME = getattr(settings, 'GOBLOG_DEFAULT_THEME', 'goblog.core.theming.Theme')
    
    # load names into the module-level namespace
    for k,v in locals().iteritems():
        if k.upper() == k and not k.startswith('_'):
            globals()[k] = v
            
def on_test_settings_change(sender=None, setting=None, value=None, **kwargs):
    load_settings()

test_signals.setting_changed.connect(on_test_settings_change)
            
load_settings()

#==============================================================================#
BLOGSPACE_NAME_MAXLEN = 100
BLOG_NAME_MAXLEN = 100
ARTICLE_NAME_MAXLEN = 32  # UUID
TAG_NAME_MAXLEN = 100
ARTICLE_COMPILER_MAXLEN = 255

#==============================================================================#
