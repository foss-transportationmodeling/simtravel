#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension

arrayexample_module = Extension('_arrayexample', 
                            sources=['arrayexample_wrap.c', 'arrayexample.c'],
                            )
                            
setup (name = 'arrayexample',
        version = '0.1',
        author = "SWIG Docs",
        description = """Simple swig example from docs""",
        ext_modules = [arrayexample_module],
        py_modules = ["arrayexample"],
        )
