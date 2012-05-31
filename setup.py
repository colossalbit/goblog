import os
import os.path
    
##from distutils.core import setup

from setuptools import setup, find_packages

# def get_subpackages(path, pkgname):
    # packages = []
    # for name in os.listdir(path):
        # subpath = os.path.join(path, name)
        # if os.path.isdir(subpath) and not os.path.islink(subpath):
            # if '__init__.py' in os.listdir(subpath):
                # subpkgname = '.'.join((pkgname, name))
                # packages.append(subpkgname)
                # subpackages = get_subpackages(subpath, subpkgname)
                # packages.extend(subpackages)
    # return packages

# def find_packages():
    # dirname = os.path.abspath(os.path.dirname(__file__))
    # path = os.path.join(dirname, 'goblog')
    # pkgname = 'goblog'
    # packages = [pkgname]
    # subpackages = get_subpackages(path, pkgname)
    # packages.extend(subpackages)
    # return packages

# goblog/__init__.py doesn't use any django modules, so the following is okay 
# even though we haven't defined DJANGO_SETTINGS_MODULE.
import goblog

THISDIR = os.path.abspath(os.path.dirname(__file__))

def read_requirements(fname):
    fpath = os.path.join(THISDIR, fname)
    with open(fpath, 'r') as f:
        reqs = []
        for line in f:
            i = line.find('#')
            if i != -1:
                line = line[:i]
            if line.strip():
                reqs.append(line.strip())
    return reqs

install_requires = read_requirements('requirements.pip')
import pprint
pprint.pprint(install_requires)

setup(
    name = 'GoBlog',
    version = goblog.__version__,
    packages = find_packages(),
    include_package_data = True,
    
    install_requires = install_requires,
    zip_safe = False,
    
    author = 'David White',
    author_email = 'TODO',
    description = 'TODO',
    license='BSD',
    keywords = 'django blog blogs blogging',
    url = 'TODO',
)
