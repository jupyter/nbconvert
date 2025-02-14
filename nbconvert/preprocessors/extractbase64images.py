"""
Preprocessor to extract base64 encoded images from markdown cells and save them to files.
"""

import os
import re
from base64 import b64decode
from uuid import uuid4
from typing import Dict, Any, Tuple

from traitlets import Bool, Unicode, Set

from nbconvert.preprocessors import Preprocessor
from nbformat.notebooknode import NotebookNode


class Base64ImageExtractor(Preprocessor):
    """
    A preprocessor to extract base64-encoded images from Markdown cells and save them as files.
    """

    use_separate_dir = Bool(
        False,
        help="Whether to use a separate directory for base64 images"
    ).tag(config=True)

    output_directory_template = Unicode(
        "{notebook_name}_files",
        help="Directory to place base64 images if use_separate_dir is True"
    ).tag(config=True)

    supported_image_types = Set(
        {"png", "jpeg", "jpg", "gif", "bmp", "svg"},
        help="Set of supported image types for extraction"
    ).tag(config=True)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.path_name = ""
        self.resources_item_key = "base64_images"  # default value

    def preprocess(self, nb: NotebookNode, resources: Dict[str, Any]) -> Tuple[NotebookNode, Dict[str, Any]]:
        """
        Preprocess the notebook and initialize the output directory for base64 images.
        """
        if not isinstance(resources, dict):
            raise TypeError("Resources must be a dictionary")

        if self.use_separate_dir:
            self.path_name = self.output_directory_template.format(
                notebook_name=resources.get("unique_key", "notebook")
            )
            resources["base64_images_dir"] = self.path_name
            resources.setdefault("base64_images", {})
            self.resources_item_key = "base64_images"
        else:
            self.path_name = resources.get("output_files_dir", "output")
            self.resources_item_key = "outputs"

        # Initialize the resources dict if needed
        resources.setdefault(self.resources_item_key, {})

        return super().preprocess(nb, resources)

    def preprocess_cell(self, cell: NotebookNode, resources: Dict[str, Any], index: int) -> Tuple[NotebookNode, Dict[str, Any]]:
        """
        Extract base64 images from Markdown cells and save them to files.
        """
        if cell.cell_type != "markdown":
            return cell, resources

        pattern = r'!\[([^\]]*)\]\(data:image/([^;]+);base64,([^\)]+)\)'

        def replace_base64(match: re.Match) -> str:
            alt_text, img_type, b64_data = match.groups()
            if img_type.lower() not in self.supported_image_types:
                self.log.warning(f"Unsupported image type: {img_type}")
                return match.group(0)

            try:
                img_data = b64decode(b64_data.encode('utf-8'))
                filename = f"base64_image_{index}_{uuid4().hex[:8]}.{img_type}"
                filepath = os.path.join(self.path_name, filename)

                # Store for FilesWriter
                resources[self.resources_item_key][filepath] = img_data

                # Return updated markdown with new image reference
                if os.path.sep != "/":
                    filepath = filepath.replace(os.path.sep, "/")
                return f"![{alt_text}]({filepath})"
            except Exception as e:
                self.log.error(f"Failed to decode base64 image: {e}")
                return match.group(0)

        cell.source = re.sub(pattern, replace_base64, cell.source)
        return cell, resources