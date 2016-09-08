"""Module containing single call export functions."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from functools import wraps
from itertools import chain
import warnings

import entrypoints

from traitlets.log import get_logger
from traitlets.utils.importstring import import_item

from nbformat import NotebookNode
from ipython_genutils.py3compat import string_types

from .exporter import Exporter
from .templateexporter import TemplateExporter
from .html import HTMLExporter
from .slides import SlidesExporter
from .latex import LatexExporter
from .pdf import PDFExporter
from .markdown import MarkdownExporter
from .python import PythonExporter
from .rst import RSTExporter
from .notebook import NotebookExporter
from .script import ScriptExporter

#-----------------------------------------------------------------------------
# Functions
#-----------------------------------------------------------------------------

__all__ = [
    'export',
    'export_by_name',
    'get_exporter',
    'get_export_names',
    'ExporterNameError',
]


class ExporterNameError(NameError):
    pass

def export(exporter, nb, **kw):
    """
    Export a notebook object using specific exporter class.
    
    Parameters
    ----------
    exporter : :class:`~nbconvert.exporters.exporter.Exporter` class or instance
      Class or instance of the exporter that should be used.  If the
      method initializes its own instance of the class, it is ASSUMED that
      the class type provided exposes a constructor (``__init__``) with the same
      signature as the base Exporter class.
    nb : :class:`~nbformat.NotebookNode`
        The notebook to export.
    config : config (optional, keyword arg)
        User configuration instance.
    resources : dict (optional, keyword arg)
        Resources used in the conversion process.

    Returns
    -------
    tuple
        output : str
            The resulting converted notebook.
        resources : dictionary
            Dictionary of resources used prior to and during the conversion 
            process.
    """
    
    #Check arguments
    if exporter is None:
        raise TypeError("Exporter is None")
    elif not isinstance(exporter, Exporter) and not issubclass(exporter, Exporter):
        raise TypeError("exporter does not inherit from Exporter (base)")
    if nb is None:
        raise TypeError("nb is None")
    
    #Create the exporter
    resources = kw.pop('resources', None)
    if isinstance(exporter, Exporter):
        exporter_instance = exporter
    else:
        exporter_instance = exporter(**kw)
    
    #Try to convert the notebook using the appropriate conversion function.
    if isinstance(nb, NotebookNode):
        output, resources = exporter_instance.from_notebook_node(nb, resources)
    elif isinstance(nb, string_types):
        output, resources = exporter_instance.from_filename(nb, resources)
    else:
        output, resources = exporter_instance.from_file(nb, resources)
    return output, resources

exporter_map = dict(
    custom=TemplateExporter,
    html=HTMLExporter,
    slides=SlidesExporter,
    latex=LatexExporter,
    pdf=PDFExporter,
    markdown=MarkdownExporter,
    python=PythonExporter,
    rst=RSTExporter,
    notebook=NotebookExporter,
    script=ScriptExporter,
)

def _make_exporter(name, E):
    """make an export_foo function from a short key and Exporter class E"""
    def _export(nb, **kw):
        return export(E, nb, **kw)
    _export.__doc__ = """DEPRECATED: Export a notebook object to {0} format""".format(name)
    return _export
    
g = globals()

# These specific functions are deprecated as of 5.0
for name, E in exporter_map.items():
    g['export_%s' % name] = _make_exporter(name, E)
    __all__.append('export_%s' % name)


def export_by_name(format_name, nb, **kw):
    """
    Deprecated since version 5.0. 

    Export a notebook object to a template type by its name.  Reflection
    (Inspect) is used to find the template's corresponding explicit export
    method defined in this module.  That method is then called directly.
    
    Parameters
    ----------
    format_name : str
        Name of the template style to export to.
    """
    
    warnings.warn("export_by_name is deprecated since nbconvert 5.0. Instead, use export(get_exporter(format_name), nb, **kw)).", DeprecationWarning, stacklevel=2)

    try:
        Exporter = get_exporter(format_name) 
        return export(Exporter, nb, **kw)
    except ValueError:
        raise ExporterNameError("Exporter for `%s` not found" % format_name)



def get_exporter(name):
    """Given an exporter name or import path, return a class ready to be instantiated
    
    Raises ValueError if exporter is not found
    """

    try:
        return entrypoints.get_single('nbconvert.exporters', name).load()
    except entrypoints.NoSuchEntryPoint:
        try:
            return entrypoints.get_single('nbconvert.exporters', name.lower()).load()
        except entrypoints.NoSuchEntryPoint:
            pass
        
    if '.' in name:
        try:
            return import_item(name)
        except ImportError:
            log = get_logger()
            log.error("Error importing %s" % name, exc_info=True)

    raise ValueError('Unknown exporter "%s", did you mean one of: %s?'
                     % (name, ', '.join(get_export_names())))


def get_export_names():
    """Return a list of the currently supported export targets
    
    Exporters can be found in external packages by registering
    them as an nbconvert.exporter entrypoint.
    """
    return sorted(exporter_map.keys()) + \
           sorted(entrypoints.get_group_named('nbconvert.exporters'))
