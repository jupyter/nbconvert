Customizing Syntax Highlighting
===============================

Under the hood, nbconvert uses pygments to highlight code. pdf, webpdf and html exporting support
changing the highlighting style.

Using Builtin styles
--------------------
Pygments has a number of builtin styles available. To use them, we just need to set the style setting
in the relevant preprocessor.

To change html and webpdf highlighting export with:

.. code-block:: bash

    jupyter nbconvert --to html notebook.ipynb --CSSHTMLHeaderPreprocessor.style=<name>

To change pdf and latex highlighting export with:

.. code-block:: bash

    jupyter nbconvert --to pdf notebook.ipynb --LatexPreprocessor.style=<name>

where ``<name>`` is the name of the pygments style. Available styles may vary from system to system.
You can find all available styles with:

.. code-block:: bash

    pygmentize -L styles

from a terminal or

.. code-block:: python

    from pygments.styles import get_all_styles
    print(list(get_all_styles()))

from python.

You can preview all the styles from an environment that can display html like jupyter notebook with:

.. code-block:: python

    from pygments.styles import get_all_styles
    from pygments.formatters import Terminal256Formatter
    from pygments.lexers import PythonLexer
    from pygments import highlight

    code = """
    import os
    def function(test=1):
        if test in [3,4]:
          print(test)
    """
    for style in get_all_styles():
        highlighted_code = highlight(code, PythonLexer(), Terminal256Formatter(style=style))
        print(f"{style}:\n{highlighted_code}")

Making your own styles
----------------------
To make your own style you must subclass ``pygments.styles.Style``, and then you must register your new style with Pygments using
their plugin system. This is explained in detail in the `Pygments documentation <http://pygments.org/docs/styles/>`_.
