import re

from django.utils import html as djhtml

from goblog import utils

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
        full, brief = self.split_brief(text)
        full = self.compile(full)
        brief = self.compile(brief)
        
        ##article_full, article_brief = self.decompose_compile_result(result)
        full = self.prepend_load_goblog_tags(full)
        if brief:
            brief = self.prepend_load_goblog_tags(brief)

        return full, brief
        
    def decompose_compile_result(self, result):
        article_brief = ''
        if isinstance(result, (list, tuple)):
            if len(result) == 1:
                article_full = result[0]
            elif len(result) == 2:
                article_full = result[0]
                article_brief = result[1]
            else:
                # TODO: Goblog-specific exception
                m = ("Configuration error: unexpected result from article "
                     "compiler.")
                raise RuntimeError(m)
        elif isinstance(result, basestring):
            article_full = result
        return article_full, article_brief
        
    def compile(self, text):
        """Take the given text and return HTML suitable for rendering in a 
        Django template.
        """
        raise NotImplementedError()
        
    def split_brief(self, text):
        """Splits the text into brief and full forms. The brief form contains 
        the text up to an 'end brief' marker, while the full form contains all 
        of the text except the 'end brief' marker.
        """
        parts = re_end_brief.split(text, maxsplit=1)
        if len(parts) == 1:
            brief = ''
            full = parts[0]
        else:
            assert len(parts) == 2
            brief = parts[0]
            full = ''.join(parts)
        return full, brief
        
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
        
    def prepend_load_goblog_tags(self, text):
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
def compile(dotted_name, rawtext):
    CompilerClass = utils.load_class(dotted_name)
    if not issubclass(CompilerClass, ArticleCompiler):
        # FIXME: raise appropriate goblog-specific exception
        raise RuntimeError("Compiler must be a subclass of ArticleCompiler.")
    compiler = CompilerClass()
    return compiler(rawtext)

#==============================================================================#

