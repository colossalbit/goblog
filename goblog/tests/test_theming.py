from goblog.core import theming

from . import base

#==============================================================================#
class Theme_TestCase(base.TestCaseBase):
    def test_basic(self):
        theme = theming.Theme()
        self.assertEqual(7, len(theme.templates))
        self.assertEqual('goblog/base.html', theme.templates['base'])
        
    def test_override(self):
        class MyTheme(theming.Theme):
            templates = {
                'base': 'path/to/mybase.html',
            }
        theme = MyTheme()
        self.assertEqual(7, len(theme.templates))
        self.assertEqual('path/to/mybase.html', theme.templates['base'])
        
    def test_merge(self):
        class MyTheme(theming.Theme):
            templates = {
                'mytemplate': 'path/to/mytemplate.html',
            }
        theme = MyTheme()
        self.assertEqual(8, len(theme.templates))
        self.assertEqual('goblog/base.html', theme.templates['base'])
        self.assertEqual('path/to/mytemplate.html', theme.templates['mytemplate'])
    
    
#==============================================================================#

