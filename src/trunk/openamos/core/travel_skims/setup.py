#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension

extending_module = Extension('_extending', 
                            sources=['extending_wrap.c', 'extending.c'],
                            )
                            
setup (name = 'extending',
        version = '0.1',
        author = "SWIG Docs",
        description = """Simple swig example from docs""",
        ext_modules = [extending_module],
        py_modules = ["extending"],
        )
