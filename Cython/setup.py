"""setup.pyx: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2013, Dilawar Singh"
__license__          = "GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import shutil

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

os.environ['CC'] = "g++"
os.environ['CXX'] = "g++"

# Clean up
moduleName = "ab"
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        if (name.startswith(moduleName) and not(name.endswith(".pyx") or
            name.endswith(".pxd") or name.endswith(".cxx"))):
            os.remove(os.path.join(root, name))
for name in dirs:
    if(name == "build"):
        shutil.rmtree(name)

setup(
        cmdclass = {'build_ext': build_ext},
        ext_modules = [
            Extension(moduleName
                , language = "C++"
                , include_dirs = [ 
                    "."
                    ]
                , sources = [
                    "ab.pyx"
                    ]
                , extra_compile_args = [ 
                    "-g"
                    , "-DCYTHON"
                    , "-DLINUX"
                    , "-DPYMOOSE"
                    ]
                , extra_link_args = ["-L."]
                , libraries = [
                    "stdc++"
                    ]
                )
            ]
    )

