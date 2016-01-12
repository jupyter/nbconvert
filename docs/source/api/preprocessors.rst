Preprocessors
=============

.. module:: nbconvert.preprocessors

.. seealso::

   :doc:`/config_options`
     Configurable options for the nbconvert application

.. autoclass:: Preprocessor

    .. automethod:: __init__

    .. automethod:: preprocess

    .. automethod:: preprocess_cell

Specialized preprocessors
-------------------------

.. autoclass:: ConvertFiguresPreprocessor

.. autoclass:: SVG2PDFPreprocessor

.. autoclass:: ExtractOutputPreprocessor

.. autoclass:: LatexPreprocessor

.. autoclass:: CSSHTMLHeaderPreprocessor

.. autoclass:: HighlightMagicsPreprocessor

.. autoclass:: ClearOutputPreprocessor

.. autoclass:: ExecutePreprocessor
    :members:

.. autofunction:: coalesce_streams
