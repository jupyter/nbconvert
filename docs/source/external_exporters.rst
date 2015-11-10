.. _external_exporter

Using external exporters
========================

.. versionadded:: 4.2

    You can now use the ``--to`` flag to use custom export formats defined in other
    libraries.


The command-line syntax to run the ``nbconvert`` script is::

  $ jupyter nbconvert --to FORMAT notebook.ipynb

This will convert the Jupyter document file ``notebook.ipynb`` into the output
format designated by the ``FORMAT`` string as explained below.

A few built-in formats are available by default: `html`, `pdf`,
`script`, `latex`. Each of these has its own _exporter_ with many configuration
options that can be extended. Having the option to point to a different _exporter_ 
allows authors to create their own fully customized templates. 

A custom _exporter_ must be a globally importable python object. We recommend that
these be distributed as python libraries.

To export using an exporter from an external library, use the `fully qualified`
name of this exporter on the command line as the argument of the ``--to`` flag::

  $ jupyter nbconvert --to <full.qualified.name> notebook.ipynb

For example, assuming a library `tcontrib` has an exporter name `TExporter`,
you would convert to this format using::
  
   $ jupyter nbconvert --to tcontrib.TExporter notebook.ipynb

A library can therefore contain multiple exporters. All other flags of the command 
line should behave the same as for built-in exporters. 


Parameters controlled by external exporter
=========================================

An external exporter can control almost any parameter of the notebook conversion
process, from simple parameters such as the output file extension, to more complex
ones such as the execution of the notebook or a custom rendering template.

All external exporters can expose custom options using the ``traitlets``
configurable API. Refer to the library that provides these exporters for 
details on how these configuration options works.

You can use the Jupyter configuration files to configure an external exporter. As
for any nbconvert exporters you can use either the configuration file syntax of
``c.MyExporter.config_option=value`` or the command line flag form
``--MyExporter.config_option=value``. 

Writing a custom ``Exporter``
=============================

Under the hood exporters are python classes that expose a certain interface. 
Any importable classes that expose this interface can be use as an exporter for
nbconvert. 

For simplicity we expose basic classes that implement all the relevant methods
that you have to subclass and overwrite just the relevant methods to provide a
custom exporter. Below we show you the step to create a custom exporter that
provides a custom file extension, and a custom template that inserts before and after
each markdown cell.

We will lay out files to be ready for Python packaging and distributing on PyPI, 
although the exact art of Python packaging is beyond the scope of this explanation. 

We will use the following layout for our package to expose a custom exporter::

    mypackage
    ├── LICENSE.md
    ├── setup.py
    └── mypackage
        ├── __init__.py
        └── templates
            └── test_template.tpl

As you can see the layout is relatively simple, in the case where a template is not 
needed we would actually have only one file with an Exporter implementation.  Of course 
you can change the layout of your package to have a more fine-grained structure of the 
subpackage. But lets see what a minimum example looks like.

We are going to write an exporter that:

  - exports to html, so we will reuse the built-in html exporter
  - changes the file extension to `.test_ext`

::
    # file __init__.py
    import os
    import os.path

    from traitlets.config import Config
    from nbconvert.exporters.html import HTMLExporter

    #-----------------------------------------------------------------------------
    # Classes
    #-----------------------------------------------------------------------------

    class MyExporter(HTMLExporter):
        """
        My custom exporter  
        """
        
        def _file_extension_default(self):
            """
            The new file extension is `.test_ext`
            """
            return '.test_ext'

        @property
        def template_path(self):
            """
            We want to inherit from HTML template, and have template under
            `./templates/` so append it to the search path. (see next section)
            """
            return super().template_path+[os.path.join(os.path.dirname(__file__), "templates")]

        def _template_file_default(self):
            """
            We want to use the new template we ship with our library.
            """
            return 'test_template' # full
        

And the template file, that inherits from the html `full` template and prepend/append text to each markdown cell (see Jinja2 docs for template syntax)::

    {% extends "full.tpl" %}

    {% block markdowncell -%}


    ## this is a markdown cells
    {super()}
    ## THIS IS THE END


    {% endblock markdowncell %}


Assuming you install this pacakge locally, or from PyPI, you can now use::

    juyter nbconvert --to mypackage.MyEporter notebook.ipynb








