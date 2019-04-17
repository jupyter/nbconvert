"""Test Pandoc module"""
#-----------------------------------------------------------------------------
#  Copyright (C) 2014 The IPython Development Team
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import os
import pytest
import warnings

from ...tests.utils import onlyif_cmds_exist

from nbconvert.tests.base import TestsBase
from testpath.tempdir import TemporaryWorkingDirectory
from .. import pandoc
from ..pandoc import replace_markdown_paths, url2pathname

#-----------------------------------------------------------------------------
# Classes and functions
#-----------------------------------------------------------------------------

class TestPandoc(TestsBase):
    """Collection of Pandoc tests"""

    def __init__(self, *args, **kwargs):
        super(TestPandoc, self).__init__(*args, **kwargs)
        self.original_env = os.environ.copy()

    def setUp(self):
        super(TestPandoc, self).setUp()
        pandoc.check_pandoc_version._cached = None

    @onlyif_cmds_exist('pandoc')
    def test_pandoc_available(self):
        """ Test behaviour that pandoc functions raise PandocMissing as documented """
        pandoc.clean_cache()

        os.environ["PATH"] = ""
        with self.assertRaises(pandoc.PandocMissing):
            pandoc.get_pandoc_version()
        with self.assertRaises(pandoc.PandocMissing):
            pandoc.check_pandoc_version()
        with self.assertRaises(pandoc.PandocMissing):
            pandoc.pandoc("", "markdown", "html")

        # original_env["PATH"] should contain pandoc
        os.environ["PATH"] = self.original_env["PATH"]
        with warnings.catch_warnings(record=True) as w:
            pandoc.get_pandoc_version()
            pandoc.check_pandoc_version()
            pandoc.pandoc("", "markdown", "html")
        self.assertEqual(w, [])

    @onlyif_cmds_exist('pandoc')
    def test_minimal_version(self):
        original_minversion = pandoc._minimal_version

        pandoc._minimal_version = "120.0"
        with warnings.catch_warnings(record=True) as w:
            # call it twice to verify the cached value is used
            assert not pandoc.check_pandoc_version()
            assert not pandoc.check_pandoc_version()
        # only one warning after two calls, due to cache
        self.assertEqual(len(w), 1)
        # clear cache
        pandoc.check_pandoc_version._cached = None
        pandoc._minimal_version = pandoc.get_pandoc_version()
        assert pandoc.check_pandoc_version()


def pandoc_function_raised_missing(f, *args, **kwargs):
    try:
        f(*args, **kwargs)
    except pandoc.PandocMissing:
        return True
    else:
        return False


@pytest.mark.parametrize(
    "test_input,expected",
    [
        # Positive cases
        ("![image](path/to/test.png)", "![image](/added/path/to/test.png)"),
        ("an ![image](path/to/test.png) with stuff", "an ![image](/added/path/to/test.png) with stuff"),
        ('an ![image](path/to/test.png "citation here") with stuff', 'an ![image](/added/path/to/test.png "citation here") with stuff'),
        ("an ![image or stuff](path/to/test.png 'citation here') with stuff", "an ![image or stuff](/added/path/to/test.png 'citation here') with stuff"),
        ("an ![image](path/to/test.png (citation here)) with stuff", "an ![image](/added/path/to/test.png (citation here)) with stuff"),
        ("an ![image](path/with spaces@test.png 'citation here') with stuff", "an ![image](/added/path/with spaces@test.png 'citation here') with stuff"),
        # Negative cases
        ("[no_explamantion](should/not/find.png)", "[no_explamantion](should/not/find.png)"),
        ("random", "random"),
        ("an ![image](path/to/test.png 'citation here'", "an ![image](path/to/test.png 'citation here'"),
        ("an ![image]path/to/test.png 'citation here')", "an ![image]path/to/test.png 'citation here')"),
        ("an ![image or stuff](/abs/path/to/test.png) with stuff", "an ![image or stuff](/abs/path/to/test.png) with stuff"),
        ('an ![image](/abs/path/to/test.png "citation here") with stuff', 'an ![image](/abs/path/to/test.png "citation here") with stuff'),
        ("an ![image](/abs/path/to/test.png 'citation here') with stuff", "an ![image](/abs/path/to/test.png 'citation here') with stuff"),
        ("an ![image](/abs/path/to/test.png (citation here)) with stuff", "an ![image](/abs/path/to/test.png (citation here)) with stuff"),
        ("an ![image](/abs/path/to/test.png 'citation here'", "an ![image](/abs/path/to/test.png 'citation here'"),
        ("an ![image]/abs/path/to/test.png) 'citation here'", "an ![image]/abs/path/to/test.png) 'citation here'"),
        ("an ![image](https://path/to/test.png) with stuff", "an ![image](https://path/to/test.png) with stuff"),
        ('an ![image](https://path/to/test.png "citation here") with stuff', 'an ![image](https://path/to/test.png "citation here") with stuff'),
        ("an ![image](https://path/to/test.png 'citation here') with stuff", "an ![image](https://path/to/test.png 'citation here') with stuff"),
        ("an ![image](https://path/to/test.png (citation here)) with stuff", "an ![image](https://path/to/test.png (citation here)) with stuff"),
        ("an ![image](https://path/to/test.png 'citation here'", "an ![image](https://path/to/test.png 'citation here'"),
        ("an ![image]https://path/to/test.png 'citation here')", "an ![image]https://path/to/test.png 'citation here')"),
    ]
)
def test_pandoc_markdown_image_rel_path_replacement(test_input, expected):
    """
    Tests that a given markdown string with "/added" passed as a relative path
    replacement is applied correctly to image links
    """
    assert replace_markdown_paths(test_input, "/added", None) == expected

@pytest.mark.parametrize(
    "test_input,expected",
    [
        # Positive cases
        ("![image](path/to/test.png)", "![image]({bd}/test.png)"),
        ("an ![image](path/to/test.png) with stuff", "an ![image]({bd}/test.png) with stuff"),
        ('an ![image](path/to/test.png "citation here") with stuff', 'an ![image]({bd}/test.png "citation here") with stuff'),
        ("an ![image or stuff](path/to/test.png 'citation here') with stuff", "an ![image or stuff]({bd}/test.png 'citation here') with stuff"),
        ("an ![image](path/to/test.png (citation here)) with stuff", "an ![image]({bd}/test.png (citation here)) with stuff"),
        ("an ![image or stuff]({td}/path/to/test.png) with stuff", "an ![image or stuff]({bd}/test.png) with stuff"),
        ('an ![image]({td}/path/to/test.png "citation here") with stuff', 'an ![image]({bd}/test.png "citation here") with stuff'),
        ("an ![image]({td}/path/to/test.png 'citation here') with stuff", "an ![image]({bd}/test.png 'citation here') with stuff"),
        ("an ![image]({td}/path/to/test.png (citation here)) with stuff", "an ![image]({bd}/test.png (citation here)) with stuff"),
        ("an ![image]({td}/path/with spaces@test.png 'citation here') with stuff", "an ![image]({bd}/with_spaces_test.png 'citation here') with stuff"),
        ("an ![image]({td}/path/with%20spaces@test.png 'citation here') with stuff", "an ![image]({bd}/with_spaces_test.png 'citation here') with stuff"),
        # Negative cases
        ("[no_explamantion](should/not/find.png)", "[no_explamantion](should/not/find.png)"),
        ("random", "random"),
        ("![image][reference_not_a_file]", "![image][reference_not_a_file]"),
        ("an ![image](path/to/test.png 'citation here'", "an ![image](path/to/test.png 'citation here'"),
        ("an ![image]path/to/test.png 'citation here')", "an ![image]path/to/test.png 'citation here')"),
        ("an ![image](/abs/path/to/test.png 'citation here'", "an ![image](/abs/path/to/test.png 'citation here'"),
        ("an ![image]/abs/path/to/test.png) 'citation here'", "an ![image]/abs/path/to/test.png) 'citation here'"),
        ("an ![image](https://path/to/test.png) with stuff", "an ![image](https://path/to/test.png) with stuff"),
        ('an ![image](https://path/to/test.png "citation here") with stuff', 'an ![image](https://path/to/test.png "citation here") with stuff'),
        ("an ![image](https://path/to/test.png 'citation here') with stuff", "an ![image](https://path/to/test.png 'citation here') with stuff"),
        ("an ![image](https://path/to/test.png (citation here)) with stuff", "an ![image](https://path/to/test.png (citation here)) with stuff"),
        ("an ![image](https://path/to/test.png 'citation here'", "an ![image](https://path/to/test.png 'citation here'"),
        ("an ![image]https://path/to/test.png 'citation here')", "an ![image]https://path/to/test.png 'citation here')"),
    ]
)
def test_pandoc_markdown_image_abs_path_copy(test_input, expected):
    """
    Tests that a given markdown link with a relative path replacement to a
    test directory `td` can link/copy image paths to a build directory `bd`.
    """
    def extract_filename(check):
        # Some hacky filters to ensure we generate empty files for all the positive tests
        if "http" not in check and '![' in check and '(' in check and ')' in check:
            fpath = check.split('(', 1)[-1].rsplit(')', 1)[0].replace('citation here', '').rsplit(' ', 1)[0]
            return url2pathname(fpath)

    with TemporaryWorkingDirectory() as td:
        test_input = test_input.format(td=td)
        fpath = extract_filename(test_input)
        # Avoid accidentally making files outside of our temp directory
        if fpath and (fpath.startswith(td) or not fpath.startswith('/')):
            # Relative paths have subdirectories
            if not os.path.exists(os.path.dirname(fpath)):
                os.makedirs(os.path.dirname(fpath))
            # We need an file on disk so the copy and rename operations work
            open(fpath, 'a').close()

        with TemporaryWorkingDirectory() as bd:
            expected = expected.format(bd=bd)
            # Prove we generated the correct path
            assert replace_markdown_paths(test_input, td, bd) == expected
            if test_input != expected:
                # Prove that if we did copy a file it exists
                assert os.path.isfile(extract_filename(expected))

@pytest.mark.parametrize(
    "test_input,expected",
    [
        # Positive cases
        ("[reference]: path/to/test.png", "[reference]: /added/path/to/test.png"),
        ("Before\n[reference]: path/to/test.png\nAfter", "Before\n[reference]: /added/path/to/test.png\nAfter"),
        (" [space]: path/to/test.png", " [space]: /added/path/to/test.png"),
        ('[reference]: path/to/test.png "citation here"', '[reference]: /added/path/to/test.png "citation here"'),
        ("[reference]: path/to/test.png 'citation here'", "[reference]: /added/path/to/test.png 'citation here'"),
        ("[reference]: path/to/test.png (citation here)", "[reference]: /added/path/to/test.png (citation here)"),
        ('[reference]: <path/to/test.png> "citation here"', '[reference]: </added/path/to/test.png> "citation here"'),
        ("[reference]: <path/to test.png> 'citation here'", "[reference]: </added/path/to test.png> 'citation here'"),
        ("[reference]: <path/to%20test.png> 'citation here'", "[reference]: </added/path/to%20test.png> 'citation here'"),
        ("[reference]: <path/to/test.png> (citation here)", "[reference]: </added/path/to/test.png> (citation here)"),
        ("[reference]:path/to/test.png", "[reference]: /added/path/to/test.png"),
        ('[reference]:path/to/test.png "citation here"', '[reference]: /added/path/to/test.png "citation here"'),
        ("[reference]:path/to/test.png 'citation here'", "[reference]: /added/path/to/test.png 'citation here'"),
        ("[reference]:path/to/test.png (citation here)", "[reference]: /added/path/to/test.png (citation here)"),
        ('[reference]:<path/to/test.png> "citation here"', '[reference]: </added/path/to/test.png> "citation here"'),
        ("[reference]:<path/to test.png> 'citation here'", "[reference]: </added/path/to test.png> 'citation here'"),
        ("[reference]:<path/to/test.png> (citation here)", "[reference]: </added/path/to/test.png> (citation here)"),
        # Negative cases
        (": not/a/reference.png", ": not/a/reference.png"),
        ("[]: not/valid/reference.png", "[]: not/valid/reference.png"),
        ("[image](not_a_ref.png)", "[image](not_a_ref.png)"),
        ('[reference]: <path/to/test.png "citation here"', '[reference]: <path/to/test.png "citation here"'),
        ('[reference]: path/to/test.png> "citation here"', '[reference]: path/to/test.png> "citation here"'),
        ("[reference]: /abs/path/to/test.png", "[reference]: /abs/path/to/test.png"),
        ('[reference]: /abs/path/to/test.png "citation here"', '[reference]: /abs/path/to/test.png "citation here"'),
        ("[reference]: /abs/path/to/test.png 'citation here'", "[reference]: /abs/path/to/test.png 'citation here'"),
        ("[reference]: /abs/path/to/test.png (citation here)", "[reference]: /abs/path/to/test.png (citation here)"),
        ('[reference]: </abs/path/to/test.png> "citation here"', '[reference]: </abs/path/to/test.png> "citation here"'),
        ("[reference]: </abs/path to/test.png> 'citation here'", "[reference]: </abs/path to/test.png> 'citation here'"),
        ("[reference]: </abs/path/to/test.png> (citation here)", "[reference]: </abs/path/to/test.png> (citation here)"),
        ('[reference]: </abs/path/with spaces/test@at space.png> "citation here"', '[reference]: </abs/path/with spaces/test@at space.png> "citation here"'),
        ("[reference]: </abs/path/to/test.png 'citation here'", "[reference]: </abs/path/to/test.png 'citation here'"),
        ("[reference]: /abs/path/to/test.png> 'citation here'", "[reference]: /abs/path/to/test.png> 'citation here'"),
        ("[reference]:/abs/path/to/test.png", "[reference]:/abs/path/to/test.png"),
        ('[reference]:/abs/path to/test.png "citation here"', '[reference]:/abs/path to/test.png "citation here"'),
        ("[reference]:/abs/path/to/test.png 'citation here'", "[reference]:/abs/path/to/test.png 'citation here'"),
        ("[reference]:/abs/path/to/test.png (citation here)", "[reference]:/abs/path/to/test.png (citation here)"),
        ('[reference]:</abs/path/to/test.png> "citation here"', '[reference]:</abs/path/to/test.png> "citation here"'),
        ("[reference]:</abs/path/to/test.png> 'citation here'", "[reference]:</abs/path/to/test.png> 'citation here'"),
        ("[reference]:</abs/path/to/test.png> (citation here)", "[reference]:</abs/path/to/test.png> (citation here)"),
        ("[reference]:</abs/path/to/test.png 'citation here'", "[reference]:</abs/path/to/test.png 'citation here'"),
        ("[reference]:/abs/path/to/test.png> 'citation here'", "[reference]:/abs/path/to/test.png> 'citation here'"),
        ("[reference]: https://path/to/test.png", "[reference]: https://path/to/test.png"),
        ('[reference]: https://path/to/test.png "citation here"', '[reference]: https://path/to/test.png "citation here"'),
        ("[reference]: https://path/to/test.png 'citation here'", "[reference]: https://path/to/test.png 'citation here'"),
        ("[reference]: https://path/to/test.png (citation here)", "[reference]: https://path/to/test.png (citation here)"),
        ('[reference]: <https://path/to/test.png> "citation here"', '[reference]: <https://path/to/test.png> "citation here"'),
        ("[reference]: <https://path/to/test.png> 'citation here'", "[reference]: <https://path/to/test.png> 'citation here'"),
        ("[reference]: <https://path/to/test.png> (citation here)", "[reference]: <https://path/to/test.png> (citation here)"),
        ("[reference]: <https://path/to/test.png 'citation here'", "[reference]: <https://path/to/test.png 'citation here'"),
        ("[reference]: https://path/to/test.png> 'citation here'", "[reference]: https://path/to/test.png> 'citation here'"),
        ("[reference]:https://path/to/test.png", "[reference]:https://path/to/test.png"),
        ('[reference]:https://path/to/test.png "citation here"', '[reference]:https://path/to/test.png "citation here"'),
        ("[reference]:https://path/to/test.png 'citation here'", "[reference]:https://path/to/test.png 'citation here'"),
        ("[reference]:https://path/to/test.png (citation here)", "[reference]:https://path/to/test.png (citation here)"),
        ('[reference]:<https://path/to/test.png> "citation here"', '[reference]:<https://path/to/test.png> "citation here"'),
        ("[reference]:<https://path/to/test.png> 'citation here'", "[reference]:<https://path/to/test.png> 'citation here'"),
        ("[reference]:<https://path/to/test.png> (citation here)", "[reference]:<https://path/to/test.png> (citation here)"),
        ("[reference]:<https://path/to/test.png 'citation here'", "[reference]:<https://path/to/test.png 'citation here'"),
        ("[reference]:https://path/to/test.png> 'citation here'", "[reference]:https://path/to/test.png> 'citation here'"),
    ])
def test_pandoc_markdown_reference_rel_path_replacement(test_input, expected):
    """
    Tests that a given markdown string with "/added" passed as a relative path
    replacement is applied correctly to image references
    """
    assert replace_markdown_paths(test_input, "/added", None) == expected

@pytest.mark.parametrize(
    "test_input,expected",
    [
        # Positive cases
        ("[reference]: path/to/test.png", "[reference]: {bd}/test.png"),
        ('[reference]: path/to/test.png "citation here"', '[reference]: {bd}/test.png "citation here"'),
        ("[reference]: path/to/test.png 'citation here'", "[reference]: {bd}/test.png 'citation here'"),
        ("[reference]: path/to/test.png (citation here)", "[reference]: {bd}/test.png (citation here)"),
        ('[reference]: <path/to/test.png> "citation here"', '[reference]: <{bd}/test.png> "citation here"'),
        ("[reference]: <path/with spaces/test.png> 'citation here'", "[reference]: <{bd}/test.png> 'citation here'"),
        ("[reference]: <path/to/test.png> (citation here)", "[reference]: <{bd}/test.png> (citation here)"),
        ('[reference]: <path/with spaces.png> "citation here"', '[reference]: <{bd}/with_spaces.png> "citation here"'),
        ('[reference]: <path/with%20spaces.png> "citation here"', '[reference]: <{bd}/with_spaces.png> "citation here"'),
        ("[reference]:path/to/test.png", "[reference]: {bd}/test.png"),
        ('[reference]:path/to/test.png "citation here"', '[reference]: {bd}/test.png "citation here"'),
        ("[reference]:path/to/test.png 'citation here'", "[reference]: {bd}/test.png 'citation here'"),
        ("[reference]:path/to/test.png (citation here)", "[reference]: {bd}/test.png (citation here)"),
        ('[reference]:<path/to/test.png> "citation here"', '[reference]: <{bd}/test.png> "citation here"'),
        ("[reference]:<path/to test.png> 'citation here'", "[reference]: <{bd}/to_test.png> 'citation here'"),
        ("[reference]:<path/to/test.png> (citation here)", "[reference]: <{bd}/test.png> (citation here)"),
        ("[reference]: {td}/path/to/test.png", "[reference]: {bd}/test.png"),
        ('[reference]: {td}/path/to/test.png "citation here"', '[reference]: {bd}/test.png "citation here"'),
        ("[reference]: {td}/path/to/test.png 'citation here'", "[reference]: {bd}/test.png 'citation here'"),
        ("[reference]: {td}/path/to/test.png (citation here)", "[reference]: {bd}/test.png (citation here)"),
        ("[reference]: <{td}/path/to/test.png> (citation here)", "[reference]: <{bd}/test.png> (citation here)"),
        ('[reference]: <{td}/path/with spaces/test@at space.png> "citation here"', '[reference]: <{bd}/test_at_space.png> "citation here"'),
        ("[reference]:{td}/path/to/test.png", "[reference]: {bd}/test.png"),
        ('[reference]:{td}/path to/test.png "citation here"', '[reference]: {bd}/test.png "citation here"'),
        ("[reference]:{td}/path/to/test.png 'citation here'", "[reference]: {bd}/test.png 'citation here'"),
        ("[reference]:{td}/path/to/test.png (citation here)", "[reference]: {bd}/test.png (citation here)"),
        ('[reference]:<{td}/path/to/test.png> "citation here"', '[reference]: <{bd}/test.png> "citation here"'),
        ("[reference]:<{td}/path/to/test.png> 'citation here'", "[reference]: <{bd}/test.png> 'citation here'"),
        ("[reference]:<{td}/path/to/test.png> (citation here)", "[reference]: <{bd}/test.png> (citation here)"),
        # Negative cases
        (": not/a/reference.png", ": not/a/reference.png"),
        ("[]: not/valid/reference.png", "[]: not/valid/reference.png"),
        ("[image](not_a_ref.png)", "[image](not_a_ref.png)"),
        ('[reference]: <path/to/test.png "citation here"', '[reference]: <path/to/test.png "citation here"'),
        ('[reference]: path/to/test.png> "citation here"', '[reference]: path/to/test.png> "citation here"'),
        ("[reference]: </abs/path/to/test.png 'citation here'", "[reference]: </abs/path/to/test.png 'citation here'"),
        ("[reference]: /abs/path/to/test.png> 'citation here'", "[reference]: /abs/path/to/test.png> 'citation here'"),
        ("[reference]:</abs/path/to/test.png 'citation here'", "[reference]:</abs/path/to/test.png 'citation here'"),
        ("[reference]:/abs/path/to/test.png> 'citation here'", "[reference]:/abs/path/to/test.png> 'citation here'"),
        ("[reference]: https://path/to/test.png", "[reference]: https://path/to/test.png"),
        ('[reference]: https://path/to/test.png "citation here"', '[reference]: https://path/to/test.png "citation here"'),
        ("[reference]: https://path/to/test.png 'citation here'", "[reference]: https://path/to/test.png 'citation here'"),
        ("[reference]: https://path/to/test.png (citation here)", "[reference]: https://path/to/test.png (citation here)"),
        ('[reference]: <https://path/to/test.png> "citation here"', '[reference]: <https://path/to/test.png> "citation here"'),
        ("[reference]: <https://path/to/test.png> 'citation here'", "[reference]: <https://path/to/test.png> 'citation here'"),
        ("[reference]: <https://path/to/test.png> (citation here)", "[reference]: <https://path/to/test.png> (citation here)"),
        ("[reference]: <https://path/to/test.png 'citation here'", "[reference]: <https://path/to/test.png 'citation here'"),
        ("[reference]: https://path/to/test.png> 'citation here'", "[reference]: https://path/to/test.png> 'citation here'"),
        ("[reference]:https://path/to/test.png", "[reference]:https://path/to/test.png"),
        ('[reference]:https://path/to/test.png "citation here"', '[reference]:https://path/to/test.png "citation here"'),
        ("[reference]:https://path/to/test.png 'citation here'", "[reference]:https://path/to/test.png 'citation here'"),
        ("[reference]:https://path/to/test.png (citation here)", "[reference]:https://path/to/test.png (citation here)"),
        ('[reference]:<https://path/to/test.png> "citation here"', '[reference]:<https://path/to/test.png> "citation here"'),
        ("[reference]:<https://path/to/test.png> 'citation here'", "[reference]:<https://path/to/test.png> 'citation here'"),
        ("[reference]:<https://path/to/test.png> (citation here)", "[reference]:<https://path/to/test.png> (citation here)"),
        ("[reference]:<https://path/to/test.png 'citation here'", "[reference]:<https://path/to/test.png 'citation here'"),
        ("[reference]:https://path/to/test.png> 'citation here'", "[reference]:https://path/to/test.png> 'citation here'"),
    ])
def test_pandoc_markdown_reference_abs_path_copy(test_input, expected):
    """
    Tests that a given markdown reference with a relative path replacement to a
    test directory `td` can link/copy image references to a build directory `bd`.
    """
    def extract_filename(check):
        # Some hacky filters to ensure we generate empty files for all the positive tests
        if "http" not in check and ']:' in check and '[]:' not in check:
            fpath = check.split(']:', 1)[-1].replace('citation here', '').strip().rsplit(' ', 1)[0]
            if '<' in fpath and '>' in fpath:
                fpath = check.split('<', 1)[-1].rsplit('>', 1)[0]
            return url2pathname(fpath.strip())

    with TemporaryWorkingDirectory() as td:
        test_input = test_input.format(td=td)
        fpath = extract_filename(test_input)
        # Avoid accidentally making files outside of our temp directory
        if fpath and (fpath.startswith(td) or not fpath.startswith('/')):
            # Relative paths have subdirectories
            if not os.path.exists(os.path.dirname(fpath)):
                os.makedirs(os.path.dirname(fpath))
            # We need an file on disk so the copy and rename operations work
            open(fpath, 'a').close()

        with TemporaryWorkingDirectory() as bd:
            expected = expected.format(bd=bd)
            # Prove we generated the correct path
            assert replace_markdown_paths(test_input, td, bd) == expected
            if test_input != expected:
                # Prove that if we did copy a file it exists
                assert os.path.isfile(extract_filename(expected))
