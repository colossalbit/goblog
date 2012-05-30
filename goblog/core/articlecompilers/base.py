import re
import collections

from django.utils import html as djhtml

from goblog import utils, appsettings

#==============================================================================#
djbracemap = {
    '{%': '{% templatetag openblock %}',
    '%}': '{% templatetag closeblock %}',
    '{{': '{% templatetag openvariable %}',
    '}}': '{% templatetag closevariable %}',
    '{':  '{% templatetag openbrace %}',
    '}':  '{% templatetag closebrace %}',
    '{#': '{% templatetag opencomment %}',
    '#}': '{% templatetag closecomment %}',
}
djbracelist = (r'\{%', r'%\}', r'\{#', r'#\}', r'\{{1,2}', r'\}{1,2}')
re_django_braces = re.compile('|'.join(djbracelist))

def escape_django_braces(m):
    return djbracemap[m.group(0)]
    

ArticleText = collections.namedtuple('ArticleText', 'brief full')
    

# end brief tag: "{{ end brief }}"
re_end_brief = re.compile(r'\{\{[ \t]*end[ \t]+brief[ \t]*\}\}')

#==============================================================================#
class ArticleCompiler(object):
    """A base class for all article compilers. """
    def __init__(self):
        pass
        
    def __call__(self, text):
        """Given the raw article input, this returns HTML to be stored in 
        database.  
        
        This calls the compile method and then adds the markup necessary to 
        load the goblog template tags.
        """
        text_start, text_end = self.split_brief(text)
        brief, full = self.compile(text_start, text_end, 
                                   target_element_id=appsettings.GOBLOG_READMORE_ELEMENT_ID)
        
        brief = self.prepend_load_goblog_tags(brief, section="brief")
        if full:
            full = self.prepend_load_goblog_tags(full, section="full")
        return ArticleText(brief, full)
        
    def compile(self, text_start, text_end, target_element_id):
        """Take the given text and return HTML suitable for rendering in a 
        Django template.  The return value is a tuple: (brief, full).  If 
        'text_end' is empty, then 'full' will also be empty.
        """
        raise NotImplementedError()
        
    def split_brief(self, text):
        """Splits the text into start and end parts. The start part contains 
        the text up to an 'end brief' marker, while the end part contains the 
        text following the 'end brief' marker.
        """
        parts = re_end_brief.split(text, maxsplit=1)
        text_start = parts[0]
        text_end = ''
        if len(parts) == 2:
            text_end = parts[1]
        return text_start, text_end
        
    def escape_braces(self, text):
        """Escapes braces that have significance in Django's templating system. 
        
        This includes: ``{{  }}  {#  #}  {%  %}  {  }``.  When rendered as a 
        Django template, the braces are unescaped by the templating system.
        
        This method is intended for use by subclasses.
        """
        return re_django_braces.sub(escape_django_braces, text)
        
    def escape_html(self, text):
        """Escapes markup of significance to HTML.
        
        This includes: ``< > &``.
        
        This method is intended for use by subclasses.
        """
        return djhtml.escape(text)
        
    def concatenate_full(self, text_start, text_end, target_element_id):
        """Concatenates the start and end text, adding a target for 
        'target_element_id' between the two.  This is intended to help 
        subclasses produce the 'full' version of the article.  
        
        If 'text_end' is empty, the return value is the empty string.  
        Otherwise, the return value will contain a ``<div>`` element.
        
        The 'text_start' and 'text_end' arguments may contain HTML.
        """
        if text_end:
            elem = "<div id='{0}'></div>".format(target_element_id)
            full = '\n'.join((text_start, elem, text_end))
        else:
            full = ''
        return full
        
    def prepend_load_goblog_tags(self, text, section=None):
        """Adds the markup necessary for Django to load the goblog template 
        tags.
        
        This method is called by the __call__ method. Subclasses should *not* 
        call prepend_load_goblog_tags, unless they override the 
        __call__ method.
        """
        return text
        # TODO: when goblog tags are implemented, use the following:
        # return u'\n'.join((u'{% load goblog %}', text))


#==============================================================================#
def resolve_article_compiler(compiler_alias):
    return appsettings.GOBLOG_ARTICLE_COMPILERS[compiler_alias]

def compile(dotted_name, rawtext):
    CompilerClass = utils.load_class(dotted_name)
    if not issubclass(CompilerClass, ArticleCompiler):
        # FIXME: raise appropriate goblog-specific exception
        raise RuntimeError("Compiler must be a subclass of ArticleCompiler.")
    compiler = CompilerClass()
    return compiler(rawtext)

#==============================================================================#

