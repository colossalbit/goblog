from django.core.exceptions import ValidationError

from . import utils

def validate_article_compiler(value):
    from .core.articlecompilers import ArticleCompiler
    
    try:
        CompilerClass = utils.load_class(value)
    except ImportError as e:
        raise ValidationError("Cannot import '{0}'.".format(value))
    
    if not issubclass(CompilerClass, ArticleCompiler):
        raise ValidationError("Not an ArticleCompiler: '{0}'.".format(value))
    




