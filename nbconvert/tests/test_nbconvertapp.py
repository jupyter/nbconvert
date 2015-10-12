# -*- coding: utf-8 -*-
"""Test NbConvertApp"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import os
import glob
import sys

from .base import TestsBase
from ..postprocessors import PostProcessorBase
from ..preprocessors.execute import CellExecutionError

from traitlets.tests.utils import check_help_all_output
from ipython_genutils.testing import decorators as dec
from nose.tools import assert_raises

#-----------------------------------------------------------------------------
# Classes and functions
#-----------------------------------------------------------------------------

class DummyPost(PostProcessorBase):
    def postprocess(self, filename):
        print("Dummy:%s" % filename)

class TestNbConvertApp(TestsBase):
    """Collection of NbConvertApp tests"""


    def test_notebook_help(self):
        """Will help show if no notebooks are specified?"""
        with self.create_temp_cwd():
            out, err = self.nbconvert('--log-level 0', ignore_return_code=True)
            self.assertIn("see '--help-all'", out)

    def test_help_output(self):
        """ipython nbconvert --help-all works"""
        check_help_all_output('nbconvert')

    def test_glob(self):
        """
        Do search patterns work for notebook names?
        """
        with self.create_temp_cwd(['notebook*.ipynb']):
            self.nbconvert('--to python *.ipynb --log-level 0')
            assert os.path.isfile('notebook1.py')
            assert os.path.isfile('notebook2.py')


    def test_glob_subdir(self):
        """
        Do search patterns work for subdirectory notebook names?
        """
        with self.create_temp_cwd():
            self.copy_files_to(['notebook*.ipynb'], 'subdir/')
            self.nbconvert('--to python --log-level 0 ' +
                      os.path.join('subdir', '*.ipynb'))
            assert os.path.isfile('notebook1.py')
            assert os.path.isfile('notebook2.py')


    def test_explicit(self):
        """
        Do explicit notebook names work?
        """
        with self.create_temp_cwd(['notebook*.ipynb']):
            self.nbconvert('--log-level 0 --to python notebook2')
            assert not os.path.isfile('notebook1.py')
            assert os.path.isfile('notebook2.py')


    @dec.onlyif_cmds_exist('pdflatex')
    @dec.onlyif_cmds_exist('pandoc')
    def test_filename_spaces(self):
        """
        Generate PDFs with graphics if notebooks have spaces in the name?
        """
        with self.create_temp_cwd(['notebook2.ipynb']):
            os.rename('notebook2.ipynb', 'notebook with spaces.ipynb')
            self.nbconvert('--log-level 0 --to pdf'
                    ' "notebook with spaces"'
                    ' --PDFExporter.latex_count=1'
                    ' --PDFExporter.verbose=True'
            )
            assert os.path.isfile('notebook with spaces.pdf')


    @dec.onlyif_cmds_exist('pdflatex')
    @dec.onlyif_cmds_exist('pandoc')
    def test_pdf(self):
        """
        Check to see if pdfs compile, even if strikethroughs are included. 
        """
        with self.create_temp_cwd(['notebook2.ipynb']):
            self.nbconvert('--log-level 0 --to pdf'
                    ' "notebook2"'
                    ' --PDFExporter.latex_count=1'
                    ' --PDFExporter.verbose=True'
            )
            assert os.path.isfile('notebook2.pdf')

    def test_post_processor(self):
        """Do post processors work?"""
        with self.create_temp_cwd(['notebook1.ipynb']):
            out, err = self.nbconvert('--log-level 0 --to python notebook1 '
                      '--post nbconvert.tests.test_nbconvertapp.DummyPost')
            self.assertIn('Dummy:notebook1.py', out)

    @dec.onlyif_cmds_exist('pandoc')
    def test_spurious_cr(self):
        """Check for extra CR characters"""
        with self.create_temp_cwd(['notebook2.ipynb']):
            self.nbconvert('--log-level 0 --to latex notebook2')
            assert os.path.isfile('notebook2.tex')
            with open('notebook2.tex') as f:
                tex = f.read()
            self.nbconvert('--log-level 0 --to html notebook2')
            assert os.path.isfile('notebook2.html')
            with open('notebook2.html') as f:
                html = f.read()
        self.assertEqual(tex.count('\r'), tex.count('\r\n'))
        self.assertEqual(html.count('\r'), html.count('\r\n'))

    @dec.onlyif_cmds_exist('pandoc')
    def test_png_base64_html_ok(self):
        """Is embedded png data well formed in HTML?"""
        with self.create_temp_cwd(['notebook2.ipynb']):
            self.nbconvert('--log-level 0 --to HTML '
                      'notebook2.ipynb --template full')
            assert os.path.isfile('notebook2.html')
            with open('notebook2.html') as f:
                assert "data:image/png;base64,b'" not in f.read()

    @dec.onlyif_cmds_exist('pandoc')
    def test_template(self):
        """
        Do export templates work?
        """
        with self.create_temp_cwd(['notebook2.ipynb']):
            self.nbconvert('--log-level 0 --to slides '
                      'notebook2.ipynb')
            assert os.path.isfile('notebook2.slides.html')
            with open('notebook2.slides.html') as f:
                assert '/reveal.css' in f.read()

    def test_output_ext(self):
        """test --output=outputfile[.ext]"""
        with self.create_temp_cwd(['notebook1.ipynb']):
            self.nbconvert('--log-level 0 --to python '
                      'notebook1.ipynb --output nb.py')
            assert os.path.exists('nb.py')

            self.nbconvert('--log-level 0 --to python '
                      'notebook1.ipynb --output nb2')
            assert os.path.exists('nb2.py')

    def test_glob_explicit(self):
        """
        Can a search pattern be used along with matching explicit notebook names?
        """
        with self.create_temp_cwd(['notebook*.ipynb']):
            self.nbconvert('--log-level 0 --to python '
                      '*.ipynb notebook1.ipynb notebook2.ipynb')
            assert os.path.isfile('notebook1.py')
            assert os.path.isfile('notebook2.py')


    def test_explicit_glob(self):
        """
        Can explicit notebook names be used and then a matching search pattern?
        """
        with self.create_temp_cwd(['notebook*.ipynb']):
            self.nbconvert('--log-level 0 --to=python '
                      'notebook1.ipynb notebook2.ipynb *.ipynb')
            assert os.path.isfile('notebook1.py')
            assert os.path.isfile('notebook2.py')


    def test_default_config(self):
        """
        Does the default config work?
        """
        with self.create_temp_cwd(['notebook*.ipynb', 'jupyter_nbconvert_config.py']):
            self.nbconvert('--log-level 0')
            assert os.path.isfile('notebook1.py')
            assert not os.path.isfile('notebook2.py')


    def test_override_config(self):
        """
        Can the default config be overriden?
        """
        with self.create_temp_cwd(['notebook*.ipynb',
                                   'jupyter_nbconvert_config.py',
                                   'override.py']):
            self.nbconvert('--log-level 0 --config="override.py"')
            assert not os.path.isfile('notebook1.py')
            assert os.path.isfile('notebook2.py')

    def test_accents_in_filename(self):
        """
        Can notebook names include accents?
        """
        with self.create_temp_cwd():
            self.create_empty_notebook(u'nb1_análisis.ipynb')
            self.nbconvert('--log-level 0 --to python nb1_*')
            assert os.path.isfile(u'nb1_análisis.py')

    @dec.onlyif_cmds_exist('pdflatex', 'pandoc')
    def test_filename_accent_pdf(self):
        """
        Generate PDFs if notebooks have an accent in their name?
        """
        with self.create_temp_cwd():
            self.create_empty_notebook(u'nb1_análisis.ipynb')
            self.nbconvert('--log-level 0 --to pdf "nb1_*"'
                    ' --PDFExporter.latex_count=1'
                    ' --PDFExporter.verbose=True')
            assert os.path.isfile(u'nb1_análisis.pdf')

    def test_cwd_plugin(self):
        """
        Verify that an extension in the cwd can be imported.
        """
        with self.create_temp_cwd(['hello.py']):
            self.create_empty_notebook(u'empty.ipynb')
            self.nbconvert('empty --to html --NbConvertApp.writer_class=\'hello.HelloWriter\'')
            assert os.path.isfile(u'hello.txt')

    def test_output_suffix(self):
        """
        Verify that the output suffix is applied
        """
        with self.create_temp_cwd():
            self.create_empty_notebook('empty.ipynb')
            self.nbconvert('empty.ipynb --to notebook')
            assert os.path.isfile('empty.nbconvert.ipynb')

    def test_different_build_dir(self):
        """
        Verify that the output suffix is not applied
        """
        with self.create_temp_cwd():
            self.create_empty_notebook('empty.ipynb')
            os.mkdir('output')
            self.nbconvert(
                'empty.ipynb --to notebook '
                '--FilesWriter.build_directory=output')
            assert os.path.isfile('output/empty.ipynb')

    def test_inplace(self):
        """
        Verify that the notebook is converted in place
        """
        with self.create_temp_cwd():
            self.create_empty_notebook('empty.ipynb')
            self.nbconvert('empty.ipynb --inplace')
            assert os.path.isfile('empty.ipynb')
            assert not os.path.isfile('empty.nbconvert.ipynb')
            assert not os.path.isfile('empty.html')

    def test_allow_errors(self):
        """
        Verify that conversion is aborted with '--execute' if an error is
        encountered, but that conversion continues if '--allow-errors' is
        used in addition.
        """
        with self.create_temp_cwd(['notebook3*.ipynb']):
            # Convert notebook containing a cell that raises an error,
            # both without and with cell execution enabled.
            output1, _ = self.nbconvert('--to markdown --stdout notebook3*.ipynb')  # no cell execution
            output2, _ = self.nbconvert('--to markdown --allow-errors --stdout notebook3*.ipynb')  # no cell execution; --allow-errors should have no effect
            output3, _ = self.nbconvert('--execute --allow-errors --to markdown --stdout notebook3*.ipynb')  # with cell execution; errors are allowed

            # Un-executed outputs should not contain either
            # of the two numbers computed in the notebook.
            assert '23' not in output1
            assert '42' not in output1
            assert '23' not in output2
            assert '42' not in output2

            # Executed output should contain both numbers.
            assert '23' in output3
            assert '42' in output3

            # Executing the notebook should raise an exception if --allow-errors is not specified
            with assert_raises(OSError):
                self.nbconvert('--execute --to markdown --stdout notebook3*.ipynb')

    def test_fenced_code_blocks_markdown(self):
        """
        Verify that input cells use fenced code blocks with the language
        name in nb.metadata.kernelspec.language, if that exists
        """
        with self.create_temp_cwd(["notebook1*.ipynb"]):
            # this notebook doesn't have nb.metadata.kernelspec, so it should
            # just do a fenced code block, with no language
            output1, _ = self.nbconvert('--to markdown --stdout notebook1.ipynb')
            assert '```python' not in output1  # shouldn't have language
            assert "```" in output1  # but should have fenced blocks

        with self.create_temp_cwd(["notebook_jl*.ipynb"]):

            output2, _ = self.nbconvert('--to markdown --stdout notebook_jl.ipynb')
            assert '```julia' in output2  # shouldn't have language
            assert "```" in output2  # but should also plain ``` to close cell

        pass

    @dec.onlyif_cmds_exist('pdflatex')
    @dec.onlyif_cmds_exist('pandoc')
    def test_linked_images(self):
        """
        Generate PDFs with an image linked in a markdown cell
        """
        with self.create_temp_cwd(['latex-linked-image.ipynb', 'testimage.png']):
            self.nbconvert('--to pdf latex-linked-image.ipynb')
            assert os.path.isfile('latex-linked-image.pdf')
