import sys

from goblog.core import articlecompilers
from goblog import appsettings

from . import base

#==============================================================================#
class AppSettings_TestCase(base.TestCaseBase):
    def test_GOBLOG_ARTICLE_COMPILERS(self):
        ARTICLE_COMPILERS = appsettings.GOBLOG_ARTICLE_COMPILERS
        for name, dotted_name in ARTICLE_COMPILERS.iteritems():
            module_name, sep, class_name = dotted_name.rpartition('.')
            try:
                __import__(module_name)
            except ImportError:
                fmt = ("ImportError while loading article compiler "
                       "'{0}' ('{1}').")
                self.fail(fmt.format(name, dotted_name))
            mod = sys.modules[module_name]
            if not hasattr(mod, class_name):
                fmt = ("Error while loading article compiler '{0}' ('{1}'): "
                       "Module has no attribute: '{2}'.")
                self.fail(fmt.format(name, dotted_name, class_name))
            cls = getattr(mod, class_name)
            if not isinstance(cls, type) or \
               not issubclass(cls, articlecompilers.ArticleCompiler):
                fmt = ("Error while loading article compiler '{0}' ('{1}'): "
                       "'{2}' is not a subclass of ArticleCompiler.")
                self.fail(fmt.format(name, dotted_name, class_name))

#==============================================================================#

