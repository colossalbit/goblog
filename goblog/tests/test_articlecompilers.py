from goblog.core import articlecompilers

from . import base

#==============================================================================#
class ArticleCompiler_TestCase(base.TestCaseBase):
    def test_split_brief(self):
        compiler = articlecompilers.ArticleCompiler()
        self.assertEqual(('',''), compiler.split_brief(''))
        
        s = 'Hello'
        self.assertEqual((s, ''), compiler.split_brief(s))
        
        s = 'the brief {{ end brief }} and the rest'
        p1 = 'the brief '
        p2 = ' and the rest'
        self.assertEqual((p1, p2), compiler.split_brief(s))
    
    
#==============================================================================#
class BasicArticleCompiler_TestCase(base.TestCaseBase):
    def test_compile_empty(self):
        compiler = articlecompilers.BasicArticleCompiler()
        self.assertEqual(('', ''), compiler(''))
    
    
#==============================================================================#
class NoHtmlArticleCompiler_TestCase(base.TestCaseBase):
    def test_compile_empty(self):
        compiler = articlecompilers.NoHtmlArticleCompiler()
        self.assertEqual(('', ''), compiler(''))
    
    
#==============================================================================#
class CleanHtmlArticleCompiler_TestCase(base.TestCaseBase):
    def test_compile_empty(self):
        compiler = articlecompilers.CleanHtmlArticleCompiler()
        self.assertEqual(('', ''), compiler(''))

#==============================================================================#

