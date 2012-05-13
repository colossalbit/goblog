from . import base



class BasicArticleCompiler(base.ArticleCompiler):
    """A basic ArticleCompiler. It performs minimal escaping and no sanitizing. 
    
    It escapes braces so Django will not interpret them in templates.  However, 
    everything else is passed on without modifications.
    """
    def compile(self, text):
        text = self.escape_braces(text)
        return text
        
        
class NoHtmlArticleCompiler(base.ArticleCompiler):
    """A simple but relatively safe ArticleCompiler. 
    
    It escapes braces for Django will not interpret them in templates. It also 
    escapes all characters of significance in HTML, like < and &. The result is 
    a stream of text without any special formatting.
    """
    def compile(self, text):
        text = self.escape_braces(text)
        text = self.escape_html(text)
        return text



