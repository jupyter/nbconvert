#!/usr/bin/env python
"""
autogen_config.py

Create config_options.rst, a Sphinx documentation source file.
Documents the options that may be set in nbconvert's configuration file,
jupyter_nbconvert_config.py.

"""
import os.path
from nbconvert.nbconvertapp import NbConvertApp

header = """\

.. This is an automatically generated file.
.. do not modify by hand.

Configuration options
=====================

Configuration options may be set in a file, ``~/.jupyter/jupyter_nbconvert_config.py``,
or at the command line when starting nbconvert, i.e. ``jupyter nbconvert --Application.log_level=10``.
"""

try:
    indir = os.path.dirname(__file__)
except NameError:
    indir = os.path.dirname(os.getcwd())
destination = os.path.join(indir, 'source/config_options.rst')

with open(destination, 'w') as f:
    f.write(header)
    f.write(NbConvertApp().document_config_options())
