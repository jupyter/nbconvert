"""Tests for the extractoutput preprocessor"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import json
import os

from nbformat import v4 as nbformat

from nbconvert.preprocessors.extractoutput import ExtractOutputPreprocessor

from .base import PreprocessorTestsBase


class TestExtractOutput(PreprocessorTestsBase):
    """Contains test functions for extractoutput.py"""

    def build_preprocessor(self):
        """Make an instance of a preprocessor"""
        preprocessor = ExtractOutputPreprocessor()
        preprocessor.extract_output_types = {"text/plain", "image/png", "application/pdf"}
        preprocessor.enabled = True
        return preprocessor

    def test_constructor(self):
        """Can a ExtractOutputPreprocessor be constructed?"""
        self.build_preprocessor()

    def test_output(self):
        """Test the output of the ExtractOutputPreprocessor"""
        nb = self.build_notebook()
        res = self.build_resources()
        preprocessor = self.build_preprocessor()
        nb, res = preprocessor(nb, res)
        # Check if text was extracted.
        output = nb.cells[0].outputs[1]
        self.assertIn("filenames", output.metadata)
        self.assertIn("text/plain", output.metadata.filenames)
        text_filename = output.metadata.filenames["text/plain"]

        # Check if png was extracted.
        output = nb.cells[0].outputs[6]
        self.assertIn("filenames", output.metadata)
        self.assertIn("image/png", output.metadata.filenames)
        png_filename = output.metadata.filenames["image/png"]

        # Check that pdf was extracted
        output = nb.cells[0].outputs[7]
        self.assertIn("filenames", output.metadata)
        self.assertIn("application/pdf", output.metadata.filenames)
        pdf_filename = output.metadata.filenames["application/pdf"]

        # Verify text output
        self.assertIn(text_filename, res["outputs"])
        self.assertEqual(res["outputs"][text_filename], b"b")

        # Verify png output
        self.assertIn(png_filename, res["outputs"])
        self.assertEqual(res["outputs"][png_filename], b"g")

        # Verify pdf output
        self.assertIn(pdf_filename, res["outputs"])
        self.assertEqual(res["outputs"][pdf_filename], b"h")

    def test_json_extraction(self):
        nb = self.build_notebook(with_json_outputs=True)
        res = self.build_resources()
        preprocessor = self.build_preprocessor()
        preprocessor.extract_output_types = {"application/json"}
        nb, res = preprocessor(nb, res)
        reference = self.build_notebook(with_json_outputs=True).cells[0].outputs

        # Verify cell untouched
        self.assertEqual(
            [out.get("data") for out in nb.cells[0].outputs], [out.get("data") for out in reference]
        )

        outputs = sorted(res["outputs"].values())
        reference_files = []
        for out in reference:
            try:
                data = out["data"]["application/json"]
                reference_files.append(json.dumps(data).encode())
            except KeyError:
                pass

        # Verify equivalence of extracted outputs.
        self.assertEqual(sorted(outputs), sorted(reference_files))

    def _extract_with_output_filename(self, filename):
        """Run the preprocessor on a notebook whose single image output carries an
        attacker-controlled ``metadata.filename``; return the resources dict."""
        output = nbformat.new_output(
            "display_data",
            data={"image/png": "Zw=="},
            metadata={"filename": filename},
        )
        nb = nbformat.new_notebook(
            cells=[nbformat.new_code_cell(source="", execution_count=1, outputs=[output])]
        )
        res = self.build_resources()
        preprocessor = self.build_preprocessor()
        _, res = preprocessor(nb, res)
        return res

    def test_output_filename_path_traversal_sanitised(self):
        """A '../' traversal in output metadata.filename must not escape the output
        directory; only the basename is used as the resource key."""
        malicious = "../../../../../../tmp/nbconvert_traversal/evil.png"
        res = self._extract_with_output_filename(malicious)
        self.assertIn("evil.png", res["outputs"])
        self.assertEqual(res["outputs"]["evil.png"], b"g")
        for key in res["outputs"]:
            self.assertNotIn("..", key)
            self.assertFalse(os.path.isabs(key))

    def test_output_filename_absolute_path_sanitised(self):
        """An absolute output metadata.filename must be reduced to its basename so
        os.path.join cannot redirect the write to an absolute location."""
        res = self._extract_with_output_filename("/tmp/absolute/evil.png")
        self.assertIn("evil.png", res["outputs"])
        self.assertNotIn("/tmp/absolute/evil.png", res["outputs"])
        self.assertEqual(res["outputs"]["evil.png"], b"g")
        for key in res["outputs"]:
            self.assertFalse(os.path.isabs(key))

    def test_output_filename_empty_basename_fallback(self):
        """A filename whose basename is empty (e.g. '../') must fall back to a
        generated filename rather than being used verbatim."""
        res = self._extract_with_output_filename("../../../tmp/")
        self.assertEqual(len(res["outputs"]), 1)
        for key in res["outputs"]:
            self.assertNotIn("..", key)
            self.assertFalse(os.path.isabs(key))
            self.assertTrue(key.endswith(".png"))
