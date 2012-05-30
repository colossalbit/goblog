from goblog import utils

#==============================================================================#
def build_dict_attribute(attrval, basevals):
    assert isinstance(attrval, dict)
    for baseval in basevals:
        baseval.update(attrval)
        attrval = baseval
    return attrval
    
def build_list_attribute(attrval, basevals):
    assert isinstance(attrval, (list, tuple))
    for baseval in basevals:
        for x in attrval:
            # Remove all x in baseval.  The 'while True' handles the case when 
            # more than one item matches x.
            try:
                while True:
                    baseval.remove(x)
            except ValueError:
                pass
        baseval.extend(attrval)
        attrval = baseval
    return attrval
    
def get_base_values(bases, attrname, do_copy=False):
    if not do_copy:
        return [ getattr(base, attrname) for base in bases 
                 if hasattr(base, attrname) ]
    else:
        return [ getattr(base, attrname).copy() for base in bases 
                 if hasattr(base, attrname) ]

    
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
        # Use 'merge_funcs' to customize how attributes are merged.
        merge_funcs = attrs.get('merge_funcs', {})
        
        for attrname in LIST_ATTRIBUTES:
            attrval = attrs.get(attrname, [])
            basevals = get_base_values(bases, attrname, do_copy=False)
            merge_func = getattr(merge_funcs, attrname, build_list_attribute)
            attrval = merge_func(attrval, basevals)
            attrs[attrname] = attrval
        
        for attrname in DICT_ATTRIBUTES:
            attrval = attrs.get(attrname, {})
            basevals = get_base_values(bases, attrname, do_copy=True)
            merge_func = getattr(merge_funcs, attrname, build_dict_attribute)
            attrval = merge_func(attrval, basevals)
            attrs[attrname] = attrval
        
        return super(ThemeMeta, mcls).__new__(mcls, name, bases, attrs)


class Theme(object):
    __metaclass__ = ThemeMeta
    
    LIST_ATTRIBUTES = ('extra_css', 'extra_js',)
    DICT_ATTRIBUTES = ('templates',)
    
    extra_css = [
        'goblog/style2.css',
        'goblog/pygments.css',
        'goblog/restructuredtext.css',
    ]
    extra_js = []
    templates = {
        'base':             'goblog/base.html',
        'goblog_base':      'goblog/goblog_base.html',
        'base_blog':        'goblog/blog/base.html',
        'blog_main':        'goblog/blog/main.html',
        'article_main':     'goblog/blog/article/main.html',
        'article_create':   'goblog/blog/article/create.html',
        'article_edit':     'goblog/blog/article/edit.html',
        'archive_month':    'goblog/blog/archives/month.html',
        'include_header':   'goblog/include/header.html',
        'include_footer':   'goblog/include/footer.html',
        'include_article':  'goblog/include/article.html',
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

