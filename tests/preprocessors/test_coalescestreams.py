"""Tests for the coalescestreams preprocessor"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from nbformat import v4 as nbformat

from nbconvert.preprocessors.coalescestreams import CoalesceStreamsPreprocessor

from .base import PreprocessorTestsBase


class TestCoalesceStreams(PreprocessorTestsBase):
    """Contains test functions for coalescestreams.py"""

    def build_preprocessor(self):
        """Make an instance of a preprocessor"""
        preprocessor = CoalesceStreamsPreprocessor()
        preprocessor.enabled = True
        return preprocessor

    def test_constructor(self):
        """Can a CoalesceStreamsPreprocessor be constructed?"""
        self.build_preprocessor()

    def process_outputs(self, outputs):
        """Process outputs"""
        cells = [nbformat.new_code_cell(source="# None", execution_count=1, outputs=outputs)]
        nb = nbformat.new_notebook(cells=cells)
        res = self.build_resources()
        preprocessor = self.build_preprocessor()
        nb, res = preprocessor(nb, res)
        return nb.cells[0].outputs

    def test_coalesce_streams(self):
        """Test the output of a CoalesceStreamsPreprocessor"""
        nb = self.build_notebook()
        outputs = self.process_outputs(nb.cells[0].outputs)
        self.assertEqual(outputs[0].text, "a")
        self.assertEqual(outputs[1].output_type, "display_data")
        self.assertEqual(outputs[2].text, "cd")
        self.assertEqual(outputs[3].text, "ef")

    def test_coalesce_sequenced_streams(self):
        """Can the coalesce streams preprocessor merge a sequence of streams?"""
        outputs = self.process_outputs(
            [
                nbformat.new_output(output_type="stream", name="stdout", text="0"),
                nbformat.new_output(output_type="stream", name="stdout", text="1"),
                nbformat.new_output(output_type="stream", name="stdout", text="2"),
                nbformat.new_output(output_type="stream", name="stdout", text="3"),
                nbformat.new_output(output_type="stream", name="stdout", text="4"),
                nbformat.new_output(output_type="stream", name="stdout", text="5"),
                nbformat.new_output(output_type="stream", name="stdout", text="6"),
                nbformat.new_output(output_type="stream", name="stdout", text="7"),
            ]
        )
        self.assertEqual(outputs[0].text, "01234567")

    def test_coalesce_replace_streams(self):
        """Are \\r characters handled?"""
        outputs = self.process_outputs(
            [
                nbformat.new_output(output_type="stream", name="stdout", text="z"),
                nbformat.new_output(output_type="stream", name="stdout", text="\ra"),
                nbformat.new_output(output_type="stream", name="stdout", text="\nz\rb"),
                nbformat.new_output(output_type="stream", name="stdout", text="\nz"),
                nbformat.new_output(output_type="stream", name="stdout", text="\rc\n"),
                nbformat.new_output(output_type="stream", name="stdout", text="z\rz\rd"),
            ]
        )
        self.assertEqual(outputs[0].text, "a\nb\nc\nd")
