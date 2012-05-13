from django.conf import settings

## GOBLOG_TAGSPACE_DEFAULT = getattr(settings, 'GOBLOG_TAGSPACE_DEFAULT', 'shared')
## # other values: 'shared', 'perblog', 'none'

GOBLOG_DEFAULT_BLOG = getattr(settings, 'GOBLOG_DEFAULT_BLOG', None)

BLOGSPACE_NAME_MAXLEN = 100
BLOG_NAME_MAXLEN = 100
ARTICLE_NAME_MAXLEN = 32  # UUID
TAG_NAME_MAXLEN = 100
ARTICLE_COMPILER_MAXLEN = 255
ARTICLE_COMPILER_DEFAULT = u'goblog.core.articlecompilers.NoHtmlArticleCompiler'

