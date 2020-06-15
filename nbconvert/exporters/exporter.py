"""This module defines a base Exporter class. For Jinja template-based export,
see templateexporter.py.
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function, absolute_import

import io
import os
import copy
import collections
import datetime

import nbformat

from traitlets.config.configurable import LoggingConfigurable
from traitlets.config import Config
from traitlets import Bool, HasTraits, Unicode, List, TraitError
from traitlets.utils.importstring import import_item
from ipython_genutils import text, py3compat


class ResourcesDict(collections.defaultdict):
    def __missing__(self, key):
        return ''


class FilenameExtension(Unicode):
    """A trait for filename extensions."""

    default_value = u''
    info_text = 'a filename extension, beginning with a dot'

    def validate(self, obj, value):
        # cast to proper unicode
        value = super().validate(obj, value)

        # check that it starts with a dot
        if value and not value.startswith('.'):
            msg = "FileExtension trait '{}' does not begin with a dot: {!r}"
            raise TraitError(msg.format(self.name, value))

        return value


class Exporter(LoggingConfigurable):
    """
    Class containing methods that sequentially run a list of processors on a
    NotebookNode object and then return the modified NotebookNode object and
    accompanying resources dict.
    """

    enabled = Bool(True,
        help = "Disable this exporter (and any exporters inherited from it)."
    ).tag(config=True)

    file_extension = FilenameExtension(
        help="Extension of the file that should be written to disk"
    ).tag(config=True)

    # MIME type of the result file, for HTTP response headers.
    # This is *not* a traitlet, because we want to be able to access it from
    # the class, not just on instances.
    output_mimetype = ''

    # Should this converter be accessible from the notebook front-end?
    # If so, should be a friendly name to display (and possibly translated).
    export_from_notebook = None

    #Configurability, allows the user to easily add filters and processors.
    processors = List(
        help="""List of processors, by name or namespace, to enable."""
    ).tag(config=True)

    _processors = List()

    default_processors = List([
                                  'nbconvert.processors.TagRemoveProcessor',
                                  'nbconvert.processors.RegexRemoveProcessor',
                                  'nbconvert.processors.ClearOutputProcessor',
                                  'nbconvert.processors.ExecuteProcessor',
                                  'nbconvert.processors.coalesce_streams',
                                  'nbconvert.processors.SVG2PDFProcessor',
                                  'nbconvert.processors.CSSHTMLHeaderProcessor',
                                  'nbconvert.processors.LatexProcessor',
                                  'nbconvert.processors.HighlightMagicsProcessor',
                                  'nbconvert.processors.ExtractOutputProcessor',
                                  'nbconvert.processors.ClearMetadataProcessor',
                              ],
        help="""List of processors available by default, by name, namespace,
        instance, or type."""
    ).tag(config=True)

    def __init__(self, config=None, **kw):
        """
        Public constructor

        Parameters
        ----------
        config : :class:`~traitlets.config.Config`
            User configuration instance.
        `**kw`
            Additional keyword arguments passed to parent __init__

        """
        with_default_config = self.default_config
        if config:
            with_default_config.merge(config)

        super().__init__(config=with_default_config, **kw)

        self._init_processors()


    @property
    def default_config(self):
        return Config()

    def from_notebook_node(self, nb, resources=None, **kw):
        """
        Convert a notebook from a notebook node instance.

        Parameters
        ----------
        nb : :class:`~nbformat.NotebookNode`
          Notebook node (dict-like with attr-access)
        resources : dict
          Additional resources that can be accessed read/write by
          processors and filters.
        `**kw`
          Ignored

        """
        nb_copy = copy.deepcopy(nb)
        resources = self._init_resources(resources)

        if 'language' in nb['metadata']:
            resources['language'] = nb['metadata']['language'].lower()

        # Process
        nb_copy, resources = self._process(nb_copy, resources)

        return nb_copy, resources


    def from_filename(self, filename, resources=None, **kw):
        """
        Convert a notebook from a notebook file.

        Parameters
        ----------
        filename : str
            Full filename of the notebook file to open and convert.
        resources : dict
          Additional resources that can be accessed read/write by
          processors and filters.
        `**kw`
          Ignored

        """
        # Convert full filename string to unicode
        # In python 2.7.x if filename comes as unicode string,
        # just skip converting it.
        if isinstance(filename, str):
           filename = py3compat.str_to_unicode(filename)

        # Pull the metadata from the filesystem.
        if resources is None:
            resources = ResourcesDict()
        if not 'metadata' in resources or resources['metadata'] == '':
            resources['metadata'] = ResourcesDict()
        path, basename = os.path.split(filename)
        notebook_name = os.path.splitext(basename)[0]
        resources['metadata']['name'] = notebook_name
        resources['metadata']['path'] = path

        modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
        resources['metadata']['modified_date'] = modified_date.strftime(text.date_format)

        with io.open(filename, encoding='utf-8') as f:
            return self.from_file(f, resources=resources, **kw)


    def from_file(self, file_stream, resources=None, **kw):
        """
        Convert a notebook from a notebook file.

        Parameters
        ----------
        file_stream : file-like object
            Notebook file-like object to convert.
        resources : dict
          Additional resources that can be accessed read/write by
          processors and filters.
        `**kw`
          Ignored

        """
        return self.from_notebook_node(nbformat.read(file_stream, as_version=4), resources=resources, **kw)


    def register_processor(self, Processor, enabled=False):
        """
        Register a Processor.
        Processor are classes that act upon the notebook before it is
        passed into the Jinja templating engine.  processors are also
        capable of passing additional information to the Jinja
        templating engine.

        Parameters
        ----------
        Processor : :class:`~nbconvert.processors.Processor`
            A dotted module name, a type, or an instance
        enabled : bool
            Mark the Processor as enabled

        """
        if Processor is None:
            raise TypeError('Processor must not be None')
        isclass = isinstance(Processor, type)
        constructed = not isclass

        # Handle Processor's registration based on it's type
        if constructed and isinstance(Processor, py3compat.string_types):
            # Processor is a string, import the namespace and recursively call
            # this register_processor method
            processor_cls = import_item(Processor)
            return self.register_processor(processor_cls, enabled)

        if constructed and hasattr(Processor, '__call__'):
            # Processor is a function, no need to construct it.
            # Register and return the Processor.
            if enabled:
                Processor.enabled = True
            self._processors.append(Processor)
            return Processor

        elif isclass and issubclass(Processor, HasTraits):
            # Processor is configurable.  Make sure to pass in new default for
            # the enabled flag if one was specified.
            self.register_processor(Processor(parent=self), enabled)

        elif isclass:
            # Processor is not configurable, construct it
            self.register_processor(Processor(), enabled)

        else:
            # Processor is an instance of something without a __call__
            # attribute.
            raise TypeError('Processor must be callable or an importable constructor, got %r' % Processor)


    def _init_processors(self):
        """
        Register all of the processors needed for this exporter, disabled
        unless specified explicitly.
        """
        self._processors = []

        # Load default processors (not necessarily enabled by default).
        for Processor in self.default_processors:
            self.register_processor(Processor)

        # Load user-specified processors.  Enable by default.
        for Processor in self.processors:
            self.register_processor(Processor, enabled=True)


    def _init_resources(self, resources):

        #Make sure the resources dict is of ResourcesDict type.
        if resources is None:
            resources = ResourcesDict()
        if not isinstance(resources, ResourcesDict):
            new_resources = ResourcesDict()
            new_resources.update(resources)
            resources = new_resources

        #Make sure the metadata extension exists in resources
        if 'metadata' in resources:
            if not isinstance(resources['metadata'], ResourcesDict):
                new_metadata = ResourcesDict()
                new_metadata.update(resources['metadata'])
                resources['metadata'] = new_metadata
        else:
            resources['metadata'] = ResourcesDict()
            if not resources['metadata']['name']:
                resources['metadata']['name'] = 'Notebook'

        #Set the output extension
        resources['output_extension'] = self.file_extension
        return resources


    def _process(self, nb, resources):
        """
        Process the notebook before passing it into the Jinja engine.
        To process the notebook is to successively apply all the
        enabled processors. Output from each Processor is passed
        along to the next one.

        Parameters
        ----------
        nb : notebook node
            notebook that is being exported.
        resources : a dict of additional resources that
            can be accessed read/write by processors
        """

        # Do a copy.deepcopy first,
        # we are never safe enough with what the processors could do.
        nbc =  copy.deepcopy(nb)
        resc = copy.deepcopy(resources)

        # Run each Processor on the notebook.  Carry the output along
        # to each Processor
        for Processor in self._processors:
            nbc, resc = Processor(nbc, resc)
            try: 
                nbformat.validate(nbc, relax_add_props=True)
            except nbformat.ValidationError:
                self.log.error('Notebook is invalid after Processor %s',
                               Processor)
                raise

        return nbc, resc
