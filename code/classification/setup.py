# # setup.py
# # from distutils.core import setup, Extension
# # from Cython.Build import cythonize
# # import numpy
# # setup(ext_modules = cythonize(Extension(
# #     'cutils',
# #     sources=['cutils.pyx'],
# #     language='c',
# #     include_dirs=[numpy.get_include()],
# #     library_dirs=[],
# #     libraries=[],
# #     extra_compile_args=[],
# #     extra_link_args=[]
# # )))

from distutils.core import setup,Extension

MOD = 'Operator' #模块名
setup(name=MOD,ext_modules=[Extension(MOD,sources=['operator_module.cpp'])])

