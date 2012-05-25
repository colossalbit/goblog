from django.core.exceptions import ValidationError

from . import utils

def validate_article_compiler(value):
    from .core.articlecompilers import ArticleCompiler, resolve_article_compiler
    try:
        dotted_name = resolve_article_compiler(value)
    except KeyError:
        raise ValidationError("Unknown compiler: '{0}'.".format(value))
    try:
        CompilerClass = utils.load_class(dotted_name)
    except ImportError as e:
        m = "Cannot import compiler '{0}' ('{1}').".format(value, dotted_name)
        raise ValidationError(m)
    
    if not issubclass(CompilerClass, ArticleCompiler):
        raise ValidationError("Not an ArticleCompiler: '{0}'.".format(value))
    




