"""Tests for the ExtractAttachments preprocessor"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import os
from base64 import b64decode, b64encode

from nbformat import v4 as nbformat

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

    def test_attachment_path_traversal_sanitised(self):
        """Test that path traversal in attachment filenames is sanitised.

        Crafted attachment filenames containing '../' sequences must not escape
        the output directory. The preprocessor should strip path components,
        store the file under its basename only, and update the cell source
        reference accordingly.
        """
        malicious_fname = "../../../../../../../tmp/nbconvert_traversal/evil.php"
        malicious_content = b"<?php\n// I should not be here"
        b64_content = b64encode(malicious_content).decode("utf-8")
        attachments = {malicious_fname: {"text/plain": b64_content}}
        cell = nbformat.new_markdown_cell(
            source=f"![exploit](attachment:{malicious_fname})",
            attachments=attachments,
        )
        nb = nbformat.new_notebook(cells=[cell])
        res = self.build_resources()
        preprocessor = self.build_preprocessor()
        nb, res = preprocessor(nb, res)

        # The output key must be the basename only - no traversal components
        self.assertIn("evil.php", res["outputs"])
        self.assertEqual(res["outputs"]["evil.php"], malicious_content)
        for key in res["outputs"]:
            self.assertNotIn("..", key)
            self.assertFalse(os.path.isabs(key))

        # Cell source must reference the safe, flattened filename
        self.assertEqual(nb.cells[0].source, "![exploit](evil.php)")

    def test_attachment_absolute_path_sanitised(self):
        """Test that absolute paths in attachment filenames are sanitised.

        An absolute path like '/tmp/absolute/test1' would cause os.path.join
        to discard the output directory prefix entirely, writing to the
        absolute location. The preprocessor must strip the path and use
        only the basename.
        """
        abs_fname = "/tmp/absolute/test1"
        content = b"absolute path write test"
        b64_content = b64encode(content).decode("utf-8")
        attachments = {abs_fname: {"text/plain": b64_content}}
        cell = nbformat.new_markdown_cell(
            source=f"![file](attachment:{abs_fname})",
            attachments=attachments,
        )
        nb = nbformat.new_notebook(cells=[cell])
        res = self.build_resources()
        preprocessor = self.build_preprocessor()
        nb, res = preprocessor(nb, res)

        # The output key must be the basename only - not the absolute path
        self.assertIn("test1", res["outputs"])
        self.assertNotIn("/tmp/absolute/test1", res["outputs"])
        self.assertEqual(res["outputs"]["test1"], content)
        for key in res["outputs"]:
            self.assertFalse(os.path.isabs(key))

        # Cell source must reference the safe, flattened filename
        self.assertEqual(nb.cells[0].source, "![file](test1)")

    def test_attachment_duplicate_filenames_are_made_unique_per_cell(self):
        """Attachments with the same filename in different cells should not overwrite.

        Markdown export writes attachments to disk, so filenames must be unique
        across cells even though notebook attachments are only scoped per cell.
        """
        first = b64encode(b"first image").decode("utf-8")
        second = b64encode(b"second image").decode("utf-8")
        first_cell = nbformat.new_markdown_cell(
            source="![first](attachment:image.png)",
            attachments={"image.png": {"image/png": first}},
        )
        second_cell = nbformat.new_markdown_cell(
            source="![second](attachment:image.png)",
            attachments={"image.png": {"image/png": second}},
        )
        nb = nbformat.new_notebook(cells=[first_cell, second_cell])
        res = self.build_resources()
        res["output_files_dir"] = "outputs"
        preprocessor = self.build_preprocessor()

        nb, res = preprocessor(nb, res)

        self.assertEqual(res["outputs"][os.path.join("outputs", "image.png")], b"first image")
        self.assertEqual(res["outputs"][os.path.join("outputs", "image_1.png")], b"second image")
        self.assertEqual(nb.cells[0].source, "![first](outputs/image.png)")
        self.assertEqual(nb.cells[1].source, "![second](outputs/image_1.png)")

    def test_attachment_sanitized_name_collisions_are_made_unique(self):
        """Sanitized basenames should still be uniquified across cells."""
        nested = b64encode(b"nested image").decode("utf-8")
        flat = b64encode(b"flat image").decode("utf-8")
        first_cell = nbformat.new_markdown_cell(
            source="![first](attachment:dir/image.png)",
            attachments={"dir/image.png": {"image/png": nested}},
        )
        second_cell = nbformat.new_markdown_cell(
            source="![second](attachment:image.png)",
            attachments={"image.png": {"image/png": flat}},
        )
        nb = nbformat.new_notebook(cells=[first_cell, second_cell])
        res = self.build_resources()
        res["output_files_dir"] = "outputs"
        preprocessor = self.build_preprocessor()

        nb, res = preprocessor(nb, res)

        self.assertEqual(res["outputs"][os.path.join("outputs", "image.png")], b"nested image")
        self.assertEqual(res["outputs"][os.path.join("outputs", "image_1.png")], b"flat image")
        self.assertEqual(nb.cells[0].source, "![first](outputs/image.png)")
        self.assertEqual(nb.cells[1].source, "![second](outputs/image_1.png)")

    def test_attachment_empty_basename_skipped(self):
        """Test that filenames resolving to an empty basename are skipped.

        A filename like '../../../tmp/' has an empty os.path.basename(),
        which would cause downstream errors if not caught. The preprocessor
        should skip these attachments entirely and log a warning.
        """
        bad_fname = "../../../tmp/"
        b64_content = b64encode(b"should be skipped").decode("utf-8")
        attachments = {bad_fname: {"text/plain": b64_content}}
        cell = nbformat.new_markdown_cell(
            source=f"![x](attachment:{bad_fname})",
            attachments=attachments,
        )
        nb = nbformat.new_notebook(cells=[cell])
        res = self.build_resources()
        preprocessor = self.build_preprocessor()
        nb, res = preprocessor(nb, res)

        # No outputs should be created for empty basename
        self.assertEqual(len(res["outputs"]), 0)

        # Cell source should remain unchanged (attachment ref not rewritten)
        self.assertEqual(nb.cells[0].source, f"![x](attachment:{bad_fname})")
