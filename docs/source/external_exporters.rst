.. _external_exporters:

Customizing exporters
=====================

.. versionadded:: 4.2

    You can now use the ``--to`` flag to use custom export formats defined
    outside nbconvert.


The command-line syntax to run the ``nbconvert`` script is::

  jupyter nbconvert --to FORMAT notebook.ipynb

This will convert the Jupyter document file ``notebook.ipynb`` into the output
format designated by the ``FORMAT`` string as explained below.

Extending the built-in format exporters
---------------------------------------
A few built-in formats are available by default: ``html``, ``pdf``, ``webpdf``,
``script``, ``latex``. Each of these has its own *exporter* with many
configuration options that can be extended. Having the option to point to a
different *exporter* allows authors to create their own fully customized
templates or export formats.

A custom *exporter* must be an importable Python object. We recommend that
these be distributed as Python libraries.

.. _entrypoints:

Registering a custom exporter as an entry point
-----------------------------------------------

Additional exporters may be registered as named entry_points_.
nbconvert uses the ``nbconvert.exporters`` entry point to find exporters
from any package you may have installed.

If you are writing a Python package that provides custom exporters,
you can register the custom exporters in your package's :file:`setup.py`. For
example, your package may contain two custom exporters, named "simple" and
"detail", and can be registered in your package's :file:`setup.py` as follows:

.. sourcecode:: python

    setup(
        ...
        entry_points = {
            'nbconvert.exporters': [
                'simple = mymodule:SimpleExporter',
                'detail = mymodule:DetailExporter',
            ],
        }
    )

Now people who have installed your Python package containing the two
custom exporters can call the entry point name::

    jupyter nbconvert --to detail mynotebook.ipynb

instead of having to specify the full import name of the custom exporter.

.. _entry_points: https://packaging.python.org/guides/
    creating-and-discovering-plugins/#using-package-metadata


Using a custom exporter without entrypoints
-------------------------------------------
We encourage registering custom exporters as entry points as described in the
previous section. Registering a custom exporter with an entry point simplifies
using the exporter. If a custom exporter has not been registered with an
entry point, the exporter can still be used by providing the fully qualified
name of this exporter as the argument of the ``--to`` flag when running from
the command line::

  $ jupyter nbconvert --to <full.qualified.name of custom exporter> notebook.ipynb

For example, assuming a library ``tcontrib`` has a custom exporter name
``TExporter``, you would convert to this custom format using the following::

   $ jupyter nbconvert --to tcontrib.TExporter notebook.ipynb

A library can contain multiple exporters. Creators of custom exporters should
make sure that all other flags of the command line behave the same for the
custom exporters as for built-in exporters.


Parameters controlled by an external exporter
=============================================

An external exporter can control almost any parameter of the notebook conversion
process, from simple parameters such as the output file extension, to more complex
ones such as the execution of the notebook or a custom rendering template.

All external exporters can expose custom options using the ``traitlets``
configurable API. Refer to the library that provides these exporters for
details on how these configuration options works.

You can use the Jupyter configuration files to configure an external exporter. As
for any ``nbconvert`` exporters you can use either the configuration file syntax of
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

If you wished to create this same directory structure you could use the following commands
when you are at the directory under which you wish to build your ``mypackage`` package:

.. code-block:: bash

    mkdir -p mypackage/mypackage/templates
    touch mypackage/LICENSE.md
    touch mypackage/setup.py
    touch mypackage/mypackage/__init__.py
    touch mypackage/mypackage/templates/test_template.tpl

.. important::
    You should not publish this package without adding content to your ``LICENSE.md`` file.
    For example, ``nbconvert`` follows the Jupyter Project convention of using a Modified BSD
    License (also known as New or Revised or 3-Clause BSD).
    For a guide on picking the right license for your use case,
    please see `choose a license <http://choosealicense.com>`_.
    If you do not specify the license, your code may be `unusable by many open source projects`_.

.. _`unusable by many open source projects`: http://choosealicense.com/no-license/

As you can see the layout is relatively simple, in the case where a template is not
needed we would actually have only one file with an Exporter implementation.  Of course
you can change the layout of your package to have a more fine-grained structure of the
subpackage. But lets see what a minimum example looks like.

We are going to write an exporter that:

  - exports to html, so we will reuse the built-in html exporter
  - changes the file extension to ``.test_ext``

.. code-block:: python

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

        # If this custom exporter should add an entry to the
        # "File -> Download as" menu in the notebook, give it a name here in the
        # `export_from_notebook` class member
        export_from_notebook = "My format"

        def _file_extension_default(self):
            """
            The new file extension is ``.test_ext``
            """
            return '.test_ext'

        @property
        def template_paths(self):
            """
            We want to inherit from HTML template, and have template under
            ``./templates/`` so append it to the search path. (see next section)

            Note: nbconvert 6.0 changed ``template_path`` to ``template_paths``
            """
            return super().template_paths+[os.path.join(os.path.dirname(__file__), "templates")]

        def _template_file_default(self):
            """
            We want to use the new template we ship with our library.
            """
            return 'test_template' # full


And the template file, that inherits from the html ``full`` template and prepend/append text to each markdown cell (see Jinja2 docs for template syntax)::

    {% extends "full.tpl" %}

    {% block markdowncell -%}


    ## this is a markdown cell
    {{ super() }}
    ## THIS IS THE END


    {% endblock markdowncell %}


Assuming you install this package locally, or from PyPI, you can now use::

    jupyter nbconvert --to mypackage.MyExporter notebook.ipynb
