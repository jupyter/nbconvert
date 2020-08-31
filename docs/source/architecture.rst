.. _architecture:

=========================
Architecture of nbconvert
=========================

This is a high-level outline of the basic workflow, structures and objects in nbconvert.
Specifically, this exposition has a two-fold goal: 
    
    #. to alert you to the affordances available for customisation or direct contributions 
    #. to provide a map of where and when different events occur, which should aid in tracking down bugs.
    

A detailed pipeline exploration
===============================

Nbconvert takes in a notebook, which is a JSON object, and operates on that object. 

This can include operations that take a notebook and return a notebook.
For example, that operation could be to execute the notebook as though it were a continuous script; if it were executed ``--in-place`` then it would overwrite the current notebook.
Or it could be that we wish to systematically alter the notebook, for example by clearing all output cells.
Format agnostic operations on cell content that do not violate the nbformat spec can be interpreted as a notebook to notebook conversion step; such operations can be performed as part of the preprocessing step.

But often we want to have the notebook's structured content in a different format.
Importantly, in many cases the structure of the notebook should be reflected in the structure of the output, adapted to the output's format.
For that purpose, the original JSON structure of the document is crucial scaffolding needed to support this kind of structured output.
In order to maintain structure, it can be useful to apply our conversion programmatically on the structure itself.
To do so, when converting to formats other than the notebook, we use the `jinja`_ templating engine.

The basic unit of structure in a notebook is the cell.
Accordingly, since our templating engine is capable of expressing structure, the basic unit in our templates will often be specified at the cell level.
Each cell has a certain type; the three most important cell types for our purposes are code, markdown, and raw NbConvert.
Code cells can be split further into their input and their output.
Operations can also occur separately on input and output and their respective subcomponents.
Markdown cells and raw NbConvert cells do not have analogous substructure.

The template's structure then can be seen as a mechanism for selecting content on which to operate.
Because the template operates on individual cells, this has some upsides and drawbacks.
One upside is that this allows the template to have access to the individual cell's metadata, which enables intelligently transforming the appropriate content. 
The transformations occur as a series of replacement rules and filters. 
For many purposes these filters take the form of external calls to `pandoc`_, which is a utility for converting between many different document formats.
One downside is that this makes operations that require global coördination (e.g., cross referencing across cells) somewhat challenging to implement as filters inside templates.

Note that all that we've described is happening in memory. 
This is crucial in order to ensure that this functionality is available when writing files is more challenging.
Nonetheless, the reason for using nbconvert almost always involves producing some kind of output file.
We take the in-memory object and write a file appropriate for the output type.

The entirety of heretofore described process can be described as part of an ``Exporter``. 
``Exporter``\s often involves ``Preprocessor``\s, ``filters``, ``templates`` and ``Writer``\s. 
These classes and functions are described in greater detail below.

Finally, one can apply a ``Postprocessor`` after the writing has occurred. 
For example, it is common when converting to slides to start a webserver and open a browser window with the newly created document (``--to slides --post serve``).

Classes
=======

.. _exporters:

Exporters
---------

The primary class in nbconvert is the `Exporter`.
Exporters encapsulate the operation of turning a notebook into another format.
There is one Exporter for each format supported in nbconvert.
The first thing an Exporter does is load a notebook, usually from a file via :mod:`nbformat`.
Most of what a typical Exporter does is select and configure preprocessors, filters, and templates.
If you want to convert notebooks to additional formats, a new Exporter is probably what you are looking for.

.. seealso::

    :ref:`Writing a custom Exporter <external_exporters>`

Once the notebook is loaded, it is preprocessed...


.. _preprocessors:

Preprocessors
-------------

A `Preprocessor` is an object that transforms the content of the notebook to be exported.
The result of a preprocessor being applied to a notebook is always a notebook.
These operations include re-executing the cells, stripping output,
removing bundled outputs to separate files, etc.
If you want to add operations that modify a notebook before exporting,
a preprocessor is the place to start.

.. seealso::

    `Custom Preprocessors <nbconvert_library.ipynb#Custom-Preprocessors>`_

Once a notebook is preprocessed, it's time to convert the notebook into the destination format.


.. _templates_and_filters:

Templates
---------

Most Exporters in nbconvert are a subclass of `TemplateExporter`, which make use of
`jinja`_ to render a notebook into the destination format.

Nbconvert templates can be selected from the command line with the ``--template``
option. For example, to use the ``reveal`` template with the HTML exporter

.. sourcecode:: bash

   jupyter nbconvert <path-to-notebook> --to html --template reveal

.. note::

   Since version 6.0, The HTML exporter defaults to the ``lab`` template which produces
   a DOM structure corresponding to the notebook component in JupyterLab.

   To produce HTML corresponding to the looks of the classic notebook, one can use the
   ``classic`` template by passing ``--template classic`` to the command line.

The nbconvert template system has been completely revamped with nbconvert 6.0 to allow
for greater extensibility. Nbconvert templates can now be installed as third-party packages
and are automatically picked up by nbconvert.

For more details about how to create custom templates, check out the :doc:`customizing` section
of the documentation.

Filters
-------

Filters are Python callables which take something (typically text) as an input, and produce a text output.
If you want to perform custom transformations of particular outputs, a filter may be the way to go.

The following code snippet is an excert from the main default template of the HTML export. The displayed
block determines how text output on ``stdout`` is displayed in HTML.

.. sourcecode:: html

    {% block stream_stdout -%}
    <div class="output_subarea output_stream output_stdout output_text">
    <pre>
    {{- output.text | ansi2html -}}
    </pre>
    </div>
    {%- endblock stream_stdout %}

In the ``{{- output.text | ansi2html -}}`` bit, we invoke the ``ansi2html`` filter to transform the text output.

Typically, filters are pure functions. However, filters that require  some configuration, may be implemented as
Configurable classes.

.. seealso::

    - :doc:`customizing`
    - :ref:`jinja:filters`

Once it has passed through the template, an Exporter is done with the notebook,
and returns the file data.

At this point, we have the file data as text or bytes and we can decide where it should end up.
When you are using nbconvert as a library, as opposed to the command-line application,
this is typically where you would stop, take your exported data, and go on your way.


.. _writers:

Writers
-------

A *Writer* takes care of writing the resulting file(s) where they should end up.
There are two basic Writers in nbconvert:

1. stdout - writes the result to stdout (for pipe-style workflows)
2. Files (default) - writes the result to the filesystem

Once the output is written, nbconvert has done its job.

.. _postprocessors:

Postprocessors
--------------

A *Postprocessor* is something that runs after everything is exported and written to the filesystem.
The only postprocessor in nbconvert at this point is the `ServePostProcessor`,
which is used for serving `reveal.js`_ HTML slideshows.

.. links:

.. _jinja: http://jinja.pocoo.org/
.. _filter: http://jinja.pocoo.org/docs/dev/templates/#filters
.. _reveal.js: http://lab.hakim.se/reveal-js
.. _pandoc: https://pandoc.org/
