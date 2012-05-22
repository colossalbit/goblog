import os
import os.path
    
from distutils.core import setup

def get_subpackages(path, pkgname):
    packages = []
    for name in os.listdir(path):
        subpath = os.path.join(path, name)
        if os.path.isdir(subpath) and not os.path.islink(subpath):
            if '__init__.py' in os.listdir(subpath):
                subpkgname = '.'.join((pkgname, name))
                packages.append(subpkgname)
                subpackages = get_subpackages(subpath, subpkgname)
                packages.extend(subpackages)
    return packages

def find_packages():
    dirname = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(dirname, 'goblog')
    pkgname = 'goblog'
    packages = [pkgname]
    subpackages = get_subpackages(path, pkgname)
    packages.extend(subpackages)
    return packages



setup(
    name='goblog',
    version='0.1',
    author='David White',
    packages=find_packages(),
)
