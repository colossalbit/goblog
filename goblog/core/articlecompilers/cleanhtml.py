import bleach

from . import base

#==============================================================================#
HTML5_ALLOWED_ELEMENTS = [
    'a',
    'abbr',
    'b',
    'blockquote',
    'br',
    'caption',
    'cite',
    'code',
    'col',
    'colgroup',
    'dd',
    'del',
    'dfn',
    'div',
    'dl',
    'dt',
    'em',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'header',
    'hgroup',
    'hr',
    'i',
    'img',
    'ins',
    'kbd',
    'li',
    'mark',
    'ol',
    'p',
    'pre',
    'q',
    'rp',   # ruby
    'rt',   # ruby
    'ruby', # ruby
    's',
    'samp',
    'small',
    'span',
    'strong',
    'sub',
    'sup',
    'table',
    'tbody',
    'td',
    'tfoot',
    'th',
    'thead',
    'time',
    'tr',
    'u',
    'ul',
    'var',
    'wbr',
]

# Elements no longer in HTML5, but that we permit.
OBSOLETE_ALLOWED_ELEMENTS = [
    'acronym', 'big', 'strike', 'tt',
]

ALLOWED_ELEMENTS_DEFAULT = HTML5_ALLOWED_ELEMENTS + OBSOLETE_ALLOWED_ELEMENTS

# Attributes allowed on any element.
ALWAYS_ALLOWED_ATTRIBUTES = [
    'class', 'id', 'title',
]

# Attributes allowed on an element-by-element basis.
ALLOWED_ATTRIBUTES_DEFAULT = {
    'a': ['href',],
    'blockquote': ['cite',],
    'ol': ['start', 'type', 'reversed',],
    'li': ['value',],
    'q': ['cite'],
    'dfn': ['title'],
    'abbr': ['title'],
    'time': ['datetime'],
    'ins': ['cite', 'datetime',],
    'del': ['cite', 'datetime',],
    'img': ['alt', 'src', 'width', 'height',],
    'colgroup': ['span',],
    'col': ['span',],
    'td': ['colspan', 'rowspan', 'headers',],
    'th': ['colspan', 'rowspan', 'headers', 'scope',],
}

ALLOWED_ATTRIBUTES_DEFAULT['*'] = ALWAYS_ALLOWED_ATTRIBUTES


#==============================================================================#
class CleanHtmlArticleCompiler(base.ArticleCompiler):
    ALLOWED_ATTRIBUTES = ALLOWED_ATTRIBUTES_DEFAULT
    ALLOWED_ELEMENTS = ALLOWED_ELEMENTS_DEFAULT
    
    def compile(self, text):
        text = self.escape_braces(text)
        text = bleach.clean(text, tags=self.ALLOWED_ELEMENTS, 
                            attributes=self.ALLOWED_ATTRIBUTES, strip=True)
        return text
        

#==============================================================================#
