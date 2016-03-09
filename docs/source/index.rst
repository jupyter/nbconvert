=============================================
nbconvert: Convert Notebooks to Other Formats
=============================================

The ``nbconvert`` tool allows you to convert an ``.ipynb`` notebook
document file into various static formats including HTML, LaTeX, PDF,
Markdown, reStructuredText, and more. The tool can also be used to execute
notebooks programmatically.

``nbconvert`` is both a python library and a command line tool. When used as
a python library (``import nbconvert``), ``nbconvert`` is useful to add
notebook conversion in your projects, such as its use to implement the 
'Download as' feature within the Jupyter Notebook web application. When used
as a command line tool (invoked as ``jupyter nbconvert ...``), users can
conveniently convert one or a batch of notebook files to another format.

Contents:

.. toctree::
   :maxdepth: 2
   :caption: User Documentation

   install
   usage
   nbconvert_library
   latex_citations
   execute_api

.. toctree::
   :maxdepth: 2
   :caption: Configuration
   
   config_options
   external_exporters
   customizing

.. toctree::
   :maxdepth: 1
   :caption: Community documentation
   
.. toctree::
   :maxdepth: 2
   :caption: Developer Documentation
   
   architecture
   api/index
   
.. toctree::
   :maxdepth: 2
   :caption: About nbconvert
   
   changelog

.. toctree::
   :maxdepth: 1
   :caption: Questions? Suggestions?

   Jupyter mailing list <https://groups.google.com/forum/#!forum/jupyter>
   Jupyter website <https://jupyter.org>
   Stack Overflow - Jupyter <https://stackoverflow.com/questions/tagged/jupyter>
   Stack Overflow - Jupyter-notebook <https://stackoverflow.com/questions/tagged/jupyter-notebook>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
