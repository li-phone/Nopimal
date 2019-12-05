# setup.py
from distutils.core import setup, Extension
from Cython.Build import cythonize

setup(
    name='Operator',
    ext_modules=cythonize(Extension(
        'Operator',
        sources=['./operator_module/operator_module.cpp'],
        language='c',
        include_dirs=[],
        library_dirs=[],
        libraries=[],
        extra_compile_args=[],
        extra_link_args=[]
    )))
