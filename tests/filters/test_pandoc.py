"""
Module with tests for Pandoc filters
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import json

from nbconvert.filters.pandoc import ConvertExplicitlyRelativePaths, convert_pandoc
from tests.base import TestsBase
from tests.testutils import onlyif_cmds_exist


class TestPandocFilters(TestsBase):
    @onlyif_cmds_exist("pandoc")
    def test_convert_explicitly_relative_paths(self):
        """
        Do the image links in a markdown file located in dir get processed correctly?
        """
        inp_dir = "/home/user/src"
        fltr = ConvertExplicitlyRelativePaths(texinputs=inp_dir)

        # pairs of input, expected
        tests = {
            # TEXINPUTS is enough, abs_path not needed
            "im.png": "im.png",
            "./im.png": "im.png",
            "./images/im.png": "images/im.png",
            # TEXINPUTS is not enough, abs_path needed
            "../im.png": "/home/user/im.png",
            "../images/im.png": "/home/user/images/im.png",
            "../../images/im.png": "/home/images/im.png",
        }

        # this shouldn't be modified by the filter
        # since it is a code block inside markdown,
        # not an image link itself
        fake = """
        ```
        \\includegraphics{../fake.png}
        ```
        """

        # convert to markdown image
        def foo(filename):
            return f"![]({filename})"

        # create input markdown and convert to pandoc json
        inp = convert_pandoc(fake + "\n".join(map(foo, tests.keys())), "markdown", "json")
        expected = convert_pandoc(fake + "\n".join(map(foo, tests.values())), "markdown", "json")
        # Do this to fix string formatting
        expected = json.dumps(json.loads(expected))
        self.assertEqual(expected, fltr(inp))

    def test_convert_explicitly_relative_paths_no_texinputs(self):
        # no texinputs should lead to just returning
        fltr = ConvertExplicitlyRelativePaths(texinputs="")
        self.assertEqual("test", fltr("test"))
