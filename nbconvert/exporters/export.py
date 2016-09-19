"""
Deprecated use nbconvert.exporters.base
"""
import warning
warning.warn("""`nbconvert.exporters.export` has been deprecated in favor of `nbconvert.exporters.base` since nbconvert 5.0.""",
             DeprecationWarning)

from .base import *

<<<<<<< HEAD
