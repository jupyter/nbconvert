Filters
=======

Filters are for use with the :class:`~nbconvert.exporters.TemplateExporter` exporter.
They provide a way for you transform notebook contents to a particular format depending
on the template you are using. For example, when converting to HTML, you would want to
use the :func:`~nbconvert.filters.ansi2html` function to convert ANSI colors (from
e.g. a terminal traceback) to HTML colors.

.. seealso::

   :doc:`/api/exporters`
     API documentation for the various exporter classes

.. module:: nbconvert.filters

.. autofunction:: add_anchor

.. autofunction:: add_prompts

.. autofunction:: ansi2html

.. autofunction:: ansi2latex

.. autofunction:: ascii_only

.. autofunction:: citation2latex

.. autofunction:: comment_lines

.. autofunction:: escape_latex

.. autoclass:: DataTypeFilter

.. autofunction:: get_lines

.. autofunction:: convert_pandoc

.. autoclass:: Highlight2HTML

.. autoclass:: Highlight2Latex

.. autofunction:: html2text

.. autofunction:: indent

.. autofunction:: ipython2python

.. autofunction:: markdown2html

.. autofunction:: markdown2latex

.. autofunction:: markdown2rst

.. autofunction:: path2url

.. autofunction:: posix_path

.. autofunction:: prevent_list_blocks

.. autofunction:: strip_ansi

.. autofunction:: strip_dollars

.. autofunction:: strip_files_prefix

.. autofunction:: wrap_text
