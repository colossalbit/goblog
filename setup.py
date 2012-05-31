##import os
##import os.path
    
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

setup(
    name = 'GoBlog',
    version = goblog.__version__,
    packages = find_packages(),
    include_package_data = True,
    
    install_requires = [],
    zip_safe = False,
    
    author = 'David White',
    author_email = 'TODO',
    description = 'TODO',
    license='BSD',
    keywords = 'django blog blogs blogging',
    url = 'TODO',
)
