import sys

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

