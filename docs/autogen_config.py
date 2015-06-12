#!/usr/bin/env python

import os.path
from nbconvert.nbconvertapp import NbConvertApp

header = """\
Configuration options
=====================

These options can be set in ``~/.jupyter/jupyter_nbconvert_config.py``, or
at the command line when you start it.
"""

try:
    indir = os.path.dirname(__file__)
except NameError:
    indir = os.path.dirname(os.getcwd())
destination = os.path.join(indir, 'source/config_options.rst')

with open(destination, 'w') as f:
    f.write(header)
    f.write(NbConvertApp().document_config_options())
