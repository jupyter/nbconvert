"""Tests for the ExtractAttachments preprocessor"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import os
from base64 import b64decode

from nbconvert.preprocessors.extractattachments import ExtractAttachmentsPreprocessor

from .base import PreprocessorTestsBase


class TestExtractAttachments(PreprocessorTestsBase):
    """Contains test functions for extractattachments.py"""

    def build_preprocessor(self):
        """Make an instance of a preprocessor"""
        preprocessor = ExtractAttachmentsPreprocessor()
        preprocessor.enabled = True
        return preprocessor

    def test_constructor(self):
        """Can a ExtractAttachmentsPreprocessor be constructed?"""
        self.build_preprocessor()

    def test_attachment(self):
        """Test the output of the ExtractAttachmentsPreprocessor"""
        nb = self.build_notebook(with_attachment=True)
        res = self.build_resources()
        preprocessor = self.build_preprocessor()
        nb, res = preprocessor(nb, res)

        # Check if attachment was extracted.
        attachments = nb.cells[-1].attachments
        self.assertIn("image.png", attachments)
        self.assertIn("image/png", attachments["image.png"])
        data = attachments["image.png"]["image/png"]
        # convert to bytes, b64 decode, convert to str
        data = b64decode(data.encode("utf-8"))
        self.assertEqual(data, b"test")

        # Verify attachment
        self.assertIn("image.png", res["outputs"])
        self.assertEqual(res["outputs"]["image.png"], b"test")

        # Verify cell source changed appropriately
        src = nb.cells[-1].source
        self.assertEqual(src, "![image.png](image.png)")

    def test_attachment_with_directory(self):
        """Test that cell source modifications are correct when files are put in a directory"""
        nb = self.build_notebook(with_attachment=True)
        res = self.build_resources()
        output_dir = "outputs"
        res["output_files_dir"] = output_dir
        preprocessor = self.build_preprocessor()
        nb, res = preprocessor(nb, res)

        # Verify attachment
        # This can have "\\" separator on Windows
        file_path = os.path.join("outputs", "image.png")
        self.assertIn(file_path, res["outputs"])

        # Verify cell source changed appropriately
        src = nb.cells[-1].source
        # This shouldn't change on Windows
        self.assertEqual(src, "![image.png](outputs/image.png)")

    def test_use_separate_dir_config(self):
        """Test that use_separate_dir and attachment_directory_template work properly"""
        nb = self.build_notebook(with_attachment=True)
        res = self.build_resources()
        res["unique_key"] = "notebook1"  # add notebook name for the folder
        preprocessor = self.build_preprocessor()
        preprocessor.use_separate_dir = True
        preprocessor.attachments_directory_template = "{notebook_name}_custom"
        nb, res = preprocessor(nb, res)

        # Verify attachment
        # This can have "\\" separator on Windows
        file_path = os.path.join("notebook1_custom", "image.png")
        self.assertIn(file_path, res["attachments"])

        # Verify cell source changed appropriately
        src = nb.cells[-1].source
        # This shouldn't change on Windows
        self.assertEqual(src, "![image.png](notebook1_custom/image.png)")
