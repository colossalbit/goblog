from . import base



class BasicArticleCompiler(base.ArticleCompiler):
    """A basic ArticleCompiler. It performs minimal escaping and no sanitizing. 
    
    It escapes braces so Django will not interpret them in templates.  However, 
    everything else is passed on without modifications.
    """
    def compile(self, text_start, text_end, target_element_id):
        brief = self.escape_braces(text_start)
        text_end = self.escape_braces(text_end)
        full = self.concatenate_full(brief, text_end, target_element_id)
        return brief, full
        
        
class NoHtmlArticleCompiler(base.ArticleCompiler):
    """A simple but relatively safe ArticleCompiler. 
    
    It escapes braces for Django will not interpret them in templates. It also 
    escapes all characters of significance in HTML, like < and &. The result is 
    a stream of text without any special formatting.
    """
    def compile(self, text_start, text_end, target_element_id):
        brief = self.escape_braces(text_start)
        brief = self.escape_html(brief)
        text_end = self.escape_braces(text_end)
        text_end = self.escape_html(text_end)
        full = self.concatenate_full(brief, text_end, target_element_id)
        return brief, full



