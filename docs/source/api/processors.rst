Processor
=============

.. module:: nbconvert.processors
   :noindex:

.. seealso::

   :doc:`/config_options`
     Configurable options for the nbconvert application

.. autoclass:: Processor

    .. automethod:: __init__

    .. automethod:: process

    .. automethod:: preprocess_cell

Specialized processors
-------------------------

Converting and extracting figures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ConvertFiguresProcessor

.. autoclass:: SVG2PDFProcessor

.. autoclass:: ExtractOutputProcessor

Converting text
~~~~~~~~~~~~~~~

.. autoclass:: LatexProcessor

.. autoclass:: HighlightMagicsProcessor

Metadata and header control
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ClearMetadataProcessor

.. autoclass:: CSSHTMLHeaderProcessor

Removing cells, inputs, and outputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ClearOutputProcessor

.. autoclass:: RegexRemoveProcessor

.. autoclass:: TagRemoveProcessor

Executing Notebooks
~~~~~~~~~~~~~~~~~~~

.. autoclass:: ExecuteProcessor
    :members:

.. autofunction:: coalesce_streams