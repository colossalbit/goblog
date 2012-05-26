import sys

from django.core.urlresolvers import reverse as urlreverse

from . import appsettings

#==============================================================================#
def import_module(dotted_module_name):
    __import__(dotted_module_name, level=0)
    mod = sys.modules[dotted_module_name]
    return mod

def load_class(dotted_name):
    module_dname, sep, class_name = dotted_name.rpartition('.')
    mod = import_module(module_dname)
    
    try :
        cls = getattr(mod, class_name)
    except AttributeError:
        m = "Name '{0}' not found in module '{1}'."
        m = m.format(classname, module_dname)
        raise ImportError(m)
    
    if not isinstance(cls, type):
        raise ImportError("'{0}' is not a class.".format(dotted_name))
    
    return cls
    
#==============================================================================#
_viewnames = {
    # each tuple: (non-default name, default name)
    'goblog-blog-main': ('goblog-blog-main', 'goblog-default-blog-main'),
    'goblog-archive-view': ('goblog-archive-view', 'goblog-default-archive-view'),
    'goblog-article-create': ('goblog-article-create', 'goblog-default-article-create'),
    'goblog-articles-view': ('goblog-articles-view', 'goblog-default-articles-view'),
    'goblog-article-view': ('goblog-article-view', 'goblog-default-article-view'),
    'goblog-article-edit': ('goblog-article-edit', 'goblog-default-article-edit'),
}

def reverse_blog_url(viewname, blogid, args=None, kwargs=None):
    try:
        nondefault_name, default_name = _viewnames[viewname]
    except KeyError:
        fmt = "Cannot reverse blog url: Not a blog view name: '{0}'"
        raise KeyError(fmt.format(viewname))
    
    kwargs = kwargs or {}
    if blogid == appsettings.GOBLOG_DEFAULT_BLOG:
        return urlreverse(default_name, args=args, kwargs=kwargs)
    else:
        kwargs['blogid'] = blogid
        return urlreverse(nondefault_name, args=args, kwargs=kwargs)
        
#==============================================================================#

