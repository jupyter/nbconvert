"""Module that pre-processes the notebook for export to HTML.
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os
import io
import hashlib
import nbconvert.resources

from traitlets import Unicode
from .base import Preprocessor


try:
    from notebook import DEFAULT_STATIC_FILES_PATH
except ImportError:
    DEFAULT_STATIC_FILES_PATH = None


class CSSHTMLHeaderPreprocessor(Preprocessor):
    """
    Preprocessor used to pre-process notebook for HTML output.  Adds IPython notebook
    front-end CSS and Pygments CSS to HTML output.
    """
    highlight_class = Unicode('.highlight',
                              help="CSS highlight class identifier"
    ).tag(config=True)

    style = Unicode('default',
            help='Name of the pygments style to use'
    ).tag(config=True)

    def __init__(self, *pargs, **kwargs):
        Preprocessor.__init__(self, *pargs, **kwargs)
        self._default_css_hash = None

    def preprocess(self, nb, resources):
        """Fetch and add CSS to the resource dictionary

        Fetch CSS from IPython and Pygments to add at the beginning
        of the html files.  Add this css in resources in the 
        "inlining.css" key
        
        Parameters
        ----------
        nb : NotebookNode
            Notebook being converted
        resources : dictionary
            Additional resources used in the conversion process.  Allows
            preprocessors to pass variables into the Jinja engine.
        """
        resources['inlining'] = {}
        resources['inlining']['css'] = self._generate_header(resources)
        return nb, resources

    def _generate_header(self, resources):
        """ 
        Fills self.header with lines of CSS extracted from IPython 
        and Pygments.
        """
        from pygments.formatters import HtmlFormatter
        header = []
        
        # Construct path to Jupyter CSS
        sheet_filename = os.path.join(
            os.path.dirname(nbconvert.resources.__file__),
            'style.min.css',
        )
        
        # Load style CSS file.
        with io.open(sheet_filename, encoding='utf-8') as f:
            header.append(f.read())

        # Add pygments CSS
        # formatter = HtmlFormatter(style=self.style)
        # pygments_css = formatter.get_style_defs(self.highlight_class)

        pygments_css = '''
.highlight .hll { background-color: var(--jp-cell-editor-active-background) }
.highlight  { background: var(--jp-cell-editor-background); }
.highlight .c { color: var(--jp-mirror-editor-comment-color) } /* Comment */
.highlight .err { color: var(--jp-mirror-editor-error-color) } /* Error */
.highlight .k { color: var(--jp-mirror-editor-keyword-color); font-weight: bold } /* Keyword */
.highlight .o { color: var(--jp-mirror-editor-operator-color) } /* Operator */
.highlight .ch { color: var(--jp-mirror-editor-comment-color) } /* Comment.Hashbang */
.highlight .cm { color: var(--jp-mirror-editor-comment-color) } /* Comment.Multiline */
.highlight .cp { color: var(--jp-mirror-editor-comment-color) } /* Comment.Preproc */
.highlight .cpf { color: var(--jp-mirror-editor-comment-color) } /* Comment.PreprocFile */
.highlight .c1 { color: var(--jp-mirror-editor-comment-color) } /* Comment.Single */
.highlight .cs { color: var(--jp-mirror-editor-comment-color) } /* Comment.Special */
.highlight .kc { color: var(--jp-mirror-editor-keyword-color); font-weight: bold } /* Keyword.Constant */
.highlight .kd { color: var(--jp-mirror-editor-keyword-color); font-weight: bold } /* Keyword.Declaration */
.highlight .kn { color: var(--jp-mirror-editor-keyword-color); font-weight: bold } /* Keyword.Namespace */
.highlight .kp { color: var(--jp-mirror-editor-keyword-color); font-weight: bold } /* Keyword.Pseudo */
.highlight .kr { color: var(--jp-mirror-editor-keyword-color); font-weight: bold } /* Keyword.Reserved */
.highlight .kt { color: var(--jp-mirror-editor-keyword-color); font-weight: bold } /* Keyword.Type */
.highlight .m { color: var(--jp-mirror-editor-number-color); font-weight: bold } /* Literal.Number */
.highlight .s { color: var(--jp-mirror-editor-string-color) } /* Literal.String */
.highlight .ow { color: var(--jp-mirror-editor-operator-color) } /* Operator.Word */
.highlight .mb { color: var(--jp-mirror-editor-number-color); font-weight: bold } /* Literal.Number.Bin */
.highlight .mf { color: var(--jp-mirror-editor-number-color); font-weight: bold } /* Literal.Number.Float */
.highlight .mh { color: var(--jp-mirror-editor-number-color); font-weight: bold } /* Literal.Number.Hex */
.highlight .mi { color: var(--jp-mirror-editor-number-color); font-weight: bold } /* Literal.Number.Integer */
.highlight .mo { color: var(--jp-mirror-editor-number-color); font-weight: bold } /* Literal.Number.Oct */
.highlight .sa { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Affix */
.highlight .sb { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Backtick */
.highlight .sc { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Char */
.highlight .dl { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Delimiter */
.highlight .sd { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Doc */
.highlight .s2 { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Double */
.highlight .se { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Escape */
.highlight .sh { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Heredoc */
.highlight .si { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Interpol */
.highlight .sx { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Other */
.highlight .sr { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Regex */
.highlight .s1 { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Single */
.highlight .ss { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Symbol */
.highlight .il { color: var(--jp-mirror-editor-number-color); font-weight: bold } /* Literal.Number.Integer.Long */
'''
        header.append(pygments_css)

        # Load the user's custom CSS and IPython's default custom CSS.  If they
        # differ, assume the user has made modifications to his/her custom CSS
        # and that we should inline it in the nbconvert output.
        config_dir = resources['config_dir']
        custom_css_filename = os.path.join(config_dir, 'custom', 'custom.css')
        if os.path.isfile(custom_css_filename):
            if DEFAULT_STATIC_FILES_PATH and self._default_css_hash is None:
                self._default_css_hash = self._hash(os.path.join(DEFAULT_STATIC_FILES_PATH, 'custom', 'custom.css'))
            if self._hash(custom_css_filename) != self._default_css_hash:
                with io.open(custom_css_filename, encoding='utf-8') as f:
                    header.append(f.read())
        return header

    def _hash(self, filename):
        """Compute the hash of a file."""
        md5 = hashlib.md5()
        with open(filename, 'rb') as f:
            md5.update(f.read())
        return md5.digest()
