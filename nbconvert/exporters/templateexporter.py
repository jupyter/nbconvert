"""This module defines TemplateExporter, a highly configurable converter
that uses Jinja2 to export notebook files into different formats.
"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function, absolute_import

import os
import uuid

# other libs/dependencies are imported at runtime
# to move ImportErrors to runtime when the requirement is actually needed

from traitlets import HasTraits, Unicode, List, Dict
from ipython_genutils.importstring import import_item
from ipython_genutils import py3compat

from nbconvert import filters
from .exporter import Exporter

#Jinja2 extensions to load.
JINJA_EXTENSIONS = ['jinja2.ext.loopcontrols']

default_filters = {
        'indent': filters.indent,
        'markdown2html': filters.markdown2html,
        'ansi2html': filters.ansi2html,
        'filter_data_type': filters.DataTypeFilter,
        'get_lines': filters.get_lines,
        'highlight2html': filters.Highlight2HTML,
        'highlight2latex': filters.Highlight2Latex,
        'ipython2python': filters.ipython2python,
        'posix_path': filters.posix_path,
        'markdown2latex': filters.markdown2latex,
        'markdown2rst': filters.markdown2rst,
        'comment_lines': filters.comment_lines,
        'strip_ansi': filters.strip_ansi,
        'strip_dollars': filters.strip_dollars,
        'strip_files_prefix': filters.strip_files_prefix,
        'html2text' : filters.html2text,
        'add_anchor': filters.add_anchor,
        'ansi2latex': filters.ansi2latex,
        'wrap_text': filters.wrap_text,
        'escape_latex': filters.escape_latex,
        'citation2latex': filters.citation2latex,
        'path2url': filters.path2url,
        'add_prompts': filters.add_prompts,
        'ascii_only': filters.ascii_only,
        'prevent_list_blocks': filters.prevent_list_blocks,
        'get_metadata': filters.get_metadata,
}


class TemplateExporter(Exporter):
    """
    Exports notebooks into other file formats.  Uses Jinja 2 templating engine
    to output new formats.  Inherit from this class if you are creating a new
    template type along with new filters/preprocessors.  If the filters/
    preprocessors provided by default suffice, there is no need to inherit from
    this class.  Instead, override the template_file and file_extension
    traits via a config file.

    {filters}
    """
    
    # finish the docstring
    __doc__ = __doc__.format(filters = '- '+'\n    - '.join(sorted(default_filters.keys())))


    _template_cached = None
    def _invalidate_template_cache(self):
        self._template_cached = None

    @property
    def template(self):
        if self._template_cached is None:
            self._template_cached = self._load_template()
        return self._template_cached

    _environment_cached = None
    def _invalidate_environment_cache(self):
        self._environment_cached = None
        self._invalidate_template_cache()

    @property
    def environment(self):
        if self._environment_cached is None:
            self._environment_cached = self._create_environment()
        return self._environment_cached

    template_file = Unicode(config=True,
            help="Name of the template file to use", affects_template=True)
    def _template_file_changed(self, name, old, new):
        if new == 'default':
            self.template_file = self.default_template

    def _template_file_default(self):
        return self.default_template

    default_template = Unicode(u'', affects_template=True)

    template_path = List(['.'], config=True, affects_template=True)

    default_template_path = Unicode(
        os.path.join("..", "templates"), 
        help="Path where the template files are located.", affects_template=True)

    template_skeleton_path = Unicode(
        os.path.join("..", "templates", "skeleton"), 
        help="Path where the template skeleton files are located.",
        affects_template=True)
    
    #Extension that the template files use.    
    template_extension = Unicode(".tpl", config=True, affects_template=True)

    extra_loaders = List(
        help="Jinja loaders to find templates. Will be tried in order "
             "before the default FileSystem ones.",
        affects_environment=True,
    )

    filters = Dict(config=True,
        help="""Dictionary of filters, by name and namespace, to add to the Jinja
        environment.""", affects_environment=True)

    raw_mimetypes = List(config=True,
        help="""formats of raw cells to be included in this Exporter's output."""
    )
    def _raw_mimetypes_default(self):
        return [self.output_mimetype, '']


    def __init__(self, config=None, **kw):
        """
        Public constructor
    
        Parameters
        ----------
        config : config
            User configuration instance.
        extra_loaders : list[of Jinja Loaders]
            ordered list of Jinja loader to find templates. Will be tried in order
            before the default FileSystem ones.
        template : str (optional, kw arg)
            Template to use when exporting.
        """
        super(TemplateExporter, self).__init__(config=config, **kw)

        self.on_trait_change(self._invalidate_environment_cache,
                     list(self.traits(affects_environment=True)))
        self.on_trait_change(self._invalidate_template_cache,
                     list(self.traits(affects_template=True)))


    def _load_template(self):
        """Load the Jinja template object from the template file
        
        This is triggered by various trait changes that would change the template.
        """
        from jinja2 import TemplateNotFound

        # Try different template names during conversion.  First try to load the
        # template by name with extension added, then try loading the template
        # as if the name is explicitly specified, then try the name as a 
        # 'flavor', and lastly just try to load the template by module name.
        try_names = []
        if self.template_file:
            try_names.extend([
                self.template_file + self.template_extension,
                self.template_file,
            ])
        for try_name in try_names:
            self.log.debug("Attempting to load template %s", try_name)
            try:
                template = self.environment.get_template(try_name)
            except (TemplateNotFound, IOError):
                pass
            else:
                self.log.debug("Loaded template %s", try_name)
                return template

    def from_notebook_node(self, nb, resources=None, **kw):
        """
        Convert a notebook from a notebook node instance.

        Parameters
        ----------
        nb : :class:`~nbformat.NotebookNode`
          Notebook node
        resources : dict
          Additional resources that can be accessed read/write by
          preprocessors and filters.
        """
        nb_copy, resources = super(TemplateExporter, self).from_notebook_node(nb, resources, **kw)
        resources.setdefault('raw_mimetypes', self.raw_mimetypes)

        self._load_template()

        if self.template is not None:
            output = self.template.render(nb=nb_copy, resources=resources)
        else:
            raise IOError('template file "%s" could not be found' % self.template_file)
        return output, resources

    def _register_filter(self, environ, name, jinja_filter):
        """
        Register a filter.
        A filter is a function that accepts and acts on one string.
        The filters are accessible within the Jinja templating engine.

        Parameters
        ----------
        name : str
            name to give the filter in the Jinja engine
        filter : filter
        """
        if jinja_filter is None:
            raise TypeError('filter')
        isclass = isinstance(jinja_filter, type)
        constructed = not isclass

        #Handle filter's registration based on it's type
        if constructed and isinstance(jinja_filter, py3compat.string_types):
            #filter is a string, import the namespace and recursively call
            #this register_filter method
            filter_cls = import_item(jinja_filter)
            return self._register_filter(environ, name, filter_cls)

        if constructed and hasattr(jinja_filter, '__call__'):
            #filter is a function, no need to construct it.
            environ.filters[name] = jinja_filter
            return jinja_filter

        elif isclass and issubclass(jinja_filter, HasTraits):
            #filter is configurable.  Make sure to pass in new default for
            #the enabled flag if one was specified.
            filter_instance = jinja_filter(parent=self)
            self._register_filter(environ, name, filter_instance)

        elif isclass:
            #filter is not configurable, construct it
            filter_instance = jinja_filter()
            self._register_filter(environ, name, filter_instance)

        else:
            #filter is an instance of something without a __call__
            #attribute.
            raise TypeError('filter')


    def register_filter(self, name, jinja_filter):
        """
        Register a filter.
        A filter is a function that accepts and acts on one string.  
        The filters are accessible within the Jinja templating engine.
    
        Parameters
        ----------
        name : str
            name to give the filter in the Jinja engine
        filter : filter
        """
        return self._register_filter(self.environment, name, jinja_filter)

    def default_filters(self):
        """Override in subclasses to provide extra filters.

        This should return an iterable of 2-tuples: (name, class-or-function).
        You should call the method on the parent class and include the filters
        it provides.

        If a name is repeated, the last filter provided wins. Filters from
        user-supplied config win over filters provided by classes.
        """
        return default_filters.items()

    def _create_environment(self):
        """
        Create the Jinja templating environment.
        """
        from jinja2 import Environment, ChoiceLoader, FileSystemLoader
        here = os.path.dirname(os.path.realpath(__file__))

        paths = self.template_path + \
            [os.path.join(here, self.default_template_path),
             os.path.join(here, self.template_skeleton_path)]
        loaders = self.extra_loaders + [FileSystemLoader(paths)]

        environment = Environment(
            loader= ChoiceLoader(loaders),
            extensions=JINJA_EXTENSIONS
            )

        environment.globals['uuid4'] = uuid.uuid4

        # Add default filters to the Jinja2 environment
        for key, value in self.default_filters():
            self._register_filter(environment, key, value)

        # Load user filters.  Overwrite existing filters if need be.
        if self.filters:
            for key, user_filter in self.filters.items():
                self._register_filter(environment, key, user_filter)

        return environment
