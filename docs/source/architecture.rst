.. _architecture:

=========================
Architecture of nbconvert
=========================

This is a high-level outline of the structure and objects in nbconvert,
and how they are used in the pipeline of converting a notebook to any given format.


.. _exporters:

Exporters
=========

The primary class in nbconvert is the :class:`.Exporter`.
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
=============

A :class:`.Preprocessor` is an object that transforms the content of the notebook to be exported.
The result of a preprocessor being applied to a notebook is always a notebook.
These operations include re-executing the cells, stripping output,
removing bundled outputs to separate files, etc.
If you want to add operations that modify a notebook before exporting,
a preprocessor is the place to start.

.. seealso::

    `Custom Preprocessors <nbconvert_library.html#Custom-Preprocessors>`_

Once a notebook is preprocessed, it's time to convert the notebook into the destination format.


.. _templates_and_filters:

Templates and Filters
=====================

Most Exporters in nbconvert are a subclass of :class:`.TemplateExporter`,
which means they use a `jinja`_ template to render a notebook into the destination format.
If you want to change how an exported notebook looks in an existing format,
a custom template is the place to start.

A jinja template is composed of blocks that look like this
(taken from nbconvert's default html template):

.. sourcecode:: html

    {% block stream_stdout -%}
    <div class="output_subarea output_stream output_stdout output_text">
    <pre>
    {{- output.text | ansi2html -}}
    </pre>
    </div>
    {%- endblock stream_stdout %}

This block determines how text output on ``stdout`` is displayed in HTML.
The ``{{- output.text | ansi2html -}}`` bit means
"Take the output text and pass it through ansi2html, then include the result here."
In this example, ``ansi2html`` is a `filter`_.
Filters are a jinja concept; they are Python callables which take something (typically text) as an input, and produce a text output.
If you want to perform new or more complex transformations of particular outputs,
a filter may be what you need.
Typically, filters are pure functions.
However, if you have a filter that itself requires some configuration,
it can be an instance of a callable, configurable class.

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
=======

A :class:`.Writer` takes care of writing the resulting file(s) where they should end up.
There are two basic Writers in nbconvert:

1. stdout - writes the result to stdout (for pipe-style workflows)
2. Files (default) - writes the result to the filesystem

Once the output is written, nbconvert has done its job.

.. _postprocessors:

Postprocessors
==============

A :class:`.Postprocessor` is something that runs after everything is exported and written to the filesystem.
The only postprocessor in nbconvert at this point is the :class:`.ServePostProcessor`,
which is used for serving `reveal.js`_ HTML slideshows.


.. links:

.. _jinja: http://jinja.pocoo.org/
.. _filter: http://jinja.pocoo.org/docs/dev/templates/#filters
.. _reveal.js: http://lab.hakim.se/reveal-js
