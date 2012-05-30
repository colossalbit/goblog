from xml.etree import ElementTree
from textwrap import dedent
import StringIO

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
class ReStructuredTextArticleCompiler_TestCase(base.TestCaseBase):
    def test_compile_empty(self):
        compiler = articlecompilers.ReStructuredTextArticleCompiler()
        self.assertEqual(('', ''), compiler(''))
        
    def test_compile1(self):
        source = """\
        Header1
        =======
        
        Paragraph1 is here.
        """
        compiler = articlecompilers.ReStructuredTextArticleCompiler()
        start, end = compiler(dedent(source))
        self.assertEqual('', end)
        stream = StringIO.StringIO(start)
        try:
            doc = ElementTree.parse(stream)
        except:
            print '\nxml document:\n{0}\n'.format(start)
            raise
        root = doc.getroot()
        self.assertEqual(None, root.find('html'))  # no html elem
        self.assertEqual(None, root.find('head'))  # no head elem
        self.assertEqual(None, root.find('body'))  # no body elem
        self.assertEqual('div', root.tag)

#==============================================================================#

