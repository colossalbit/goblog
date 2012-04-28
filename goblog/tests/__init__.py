import os
import os.path
import sys
import re

from django.utils import unittest

TESTMOD_PREFIX = 'test_'
re_testmod = re.compile(r'^(?P<name>' + TESTMOD_PREFIX + r'[\d\w_]+)\.py$')

DIRNAME = os.path.dirname(__file__)
assert __package__
TESTSPKG = __package__

def find_test_modules():
    modinfo = []
    for name in os.listdir(DIRNAME):
        fullname = os.path.join(DIRNAME, name)
        if os.path.isdir(fullname):
            # ignore sub-directories
            continue
        m = re_testmod.match(name)
        if m is not None:
            modname = m.group('name')
            fullmodname = '{0}.{1}'.format(TESTSPKG, modname)
            modinfo.append((modname, fullmodname))
    ##print 'len(modinfo): {0}'.format(len(modinfo))
    ##print 'modinfo: {0}'.format(modinfo)
    return modinfo
    
def load_test_classes(mod, modname, fullmodname):
    for objname, obj in mod.__dict__.iteritems():
        if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
            ##modname.replace('.', '__')
            newclassname = '{0}__{1}'.format(modname, objname)
            attrs = sorted(obj.__dict__.keys())
            if any((attr.startswith('test')) for attr in attrs):
                assert newclassname not in globals(), 'newclassname: {0}'.format(newclassname)
                globals()[newclassname] = obj
    
    
def load_test_modules(modinfo):
    for modname, fullmodname in modinfo:
        __import__(fullmodname, globals(), locals(), [], -1)
        mod = sys.modules[fullmodname]
        load_test_classes(mod, modname, fullmodname)
        
modinfo = find_test_modules()
load_test_modules(modinfo)





