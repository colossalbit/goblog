from goblog import utils

#==============================================================================#
def build_dict_attribute(attrname, attrval, bases):
    assert isinstance(attrval, dict)
    for base in bases:
        if hasattr(base, attrname):
            baseattr = getattr(base, attrname).copy()
            baseattr.update(attrval)
            attrval = baseattr
    return attrval
    
def build_list_attribute(attrname, attrval, bases):
    assert isinstance(attrval, (list, tuple))
    for base in bases:
        if hasattr(base, attrname):
            baseattr = getattr(base, attrname)
            for x in attrval:
                # remove all x in baseattr
                try:
                    while True:
                        baseattr.remove(x)
                except ValueError:
                    pass
            baseattr.extend(attrval)
            attrval = baseattr
    return attrval
    
def get_inherited_theme_attr(attrs, bases, attrname):
    if attrname in attrs:
        return attrs[attrname]
    for base in bases:
        if hasattr(base, attrname):
            return getattr(base, attrname)
    raise AttributeError("Theme has no '{0}' attribute.".format(attrname))


class ThemeMeta(type):
    def __new__(mcls, name, bases, attrs):
        LIST_ATTRIBUTES = get_inherited_theme_attr(attrs, bases, 'LIST_ATTRIBUTES')
        DICT_ATTRIBUTES = get_inherited_theme_attr(attrs, bases, 'DICT_ATTRIBUTES')
        
        for attrname in LIST_ATTRIBUTES:
            attrval = attrs.get(attrname, [])
            attrval = build_list_attribute(attrname, attrval, bases)
            attrs[attrname] = attrval
        
        for attrname in DICT_ATTRIBUTES:
            attrval = attrs.get(attrname, {})
            attrval = build_dict_attribute(attrname, attrval, bases)
            attrs[attrname] = attrval
        
        return super(ThemeMeta, mcls).__new__(mcls, name, bases, attrs)


class Theme(object):
    __metaclass__ = ThemeMeta
    
    LIST_ATTRIBUTES = ('extra_css', 'extra_js',)
    DICT_ATTRIBUTES = ('templates',)
    
    extra_css = [
        'goblog/style.css',
    ]
    extra_js = []
    templates = {
        'base': 'goblog/base.html',
        'base_blog': 'goblog/blogbase.html',
        'blog_main': 'goblog/blogmain.html',
        'article_main': 'goblog/article.html',
        'article_create': 'goblog/article_create.html',
        'article_edit': 'goblog/article_edit.html',
        'archive_month': 'goblog/archive.html',
    }


#==============================================================================#
_cache = {}

def gettheme(dotted_theme_name):
    if dotted_theme_name not in _cache:
        try:
            cls = utils.load_class(dotted_theme_name)
        except Exception as e:
            m = "Unable to load theme: '{0}': {1}."
            raise RuntimeError(m.format(dotted_theme_name, str(e)))
        if not issubclass(cls, Theme):
            # FIXME: raise appropriate goblog-specific exception
            raise RuntimeError("Themes must be a subclass of Theme.")
        _cache[dotted_theme_name] = cls
    return _cache[dotted_theme_name]

#==============================================================================#

