"""Utility for calling pandoc"""
# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.


import re
import shutil
import subprocess
import warnings
from io import BytesIO, TextIOWrapper

from nbconvert.utils.version import check_version

from .exceptions import ConversionException

_minimal_version = "1.12.1"
_maximal_version = "3.0.0"


def pandoc(source, fmt, to, extra_args=None, encoding="utf-8"):
    """Convert an input string using pandoc.

    Pandoc converts an input string `from` a format `to` a target format.

    Parameters
    ----------
    source : string
        Input string, assumed to be valid format `from`.
    fmt : string
        The name of the input format (markdown, etc.)
    to : string
        The name of the output format (html, etc.)

    Returns
    -------
    out : unicode
        Output as returned by pandoc.

    Raises
    ------
    PandocMissing
        If pandoc is not installed.
    Any error messages generated by pandoc are printed to stderr.

    """
    cmd = ["pandoc", "-f", fmt, "-t", to]
    if extra_args:
        cmd.extend(extra_args)

    # this will raise an exception that will pop us out of here
    check_pandoc_version()

    # we can safely continue
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, _ = p.communicate(source.encode())
    out_str = TextIOWrapper(BytesIO(out), encoding, "replace").read()
    return out_str.rstrip("\n")


def get_pandoc_version():
    """Gets the Pandoc version if Pandoc is installed.

    If the minimal version is not met, it will probe Pandoc for its version, cache it and return that value.
    If the minimal version is met, it will return the cached version and stop probing Pandoc
    (unless `clean_cache()` is called).

    Raises
    ------
    PandocMissing
        If pandoc is unavailable.
    """
    global __version  # noqa

    if __version is None:
        if not shutil.which("pandoc"):
            raise PandocMissing()

        out = subprocess.check_output(["pandoc", "-v"])
        out_lines = out.splitlines()
        version_pattern = re.compile(r"^\d+(\.\d+){1,}$")
        for tok in out_lines[0].decode("ascii", "replace").split():
            if version_pattern.match(tok):
                __version = tok  # type:ignore
                break
    return __version


def check_pandoc_version():
    """Returns True if pandoc's version meets at least minimal version.

    Raises
    ------
    PandocMissing
        If pandoc is unavailable.
    """
    if check_pandoc_version._cached is not None:  # type:ignore
        return check_pandoc_version._cached  # type:ignore

    v = get_pandoc_version()
    if v is None:
        warnings.warn(
            "Sorry, we cannot determine the version of pandoc.\n"
            "Please consider reporting this issue and include the"
            "output of pandoc --version.\nContinuing...",
            RuntimeWarning,
            stacklevel=2,
        )
        return False
    ok = check_version(v, _minimal_version, max_v=_maximal_version)
    check_pandoc_version._cached = ok  # type:ignore
    if not ok:
        warnings.warn(
            "You are using an unsupported version of pandoc (%s).\n" % v
            + "Your version must be at least (%s) " % _minimal_version
            + "but less than (%s).\n" % _maximal_version
            + "Refer to https://pandoc.org/installing.html.\nContinuing with doubts...",
            RuntimeWarning,
            stacklevel=2,
        )
    return ok


check_pandoc_version._cached = None  # type:ignore

# -----------------------------------------------------------------------------
# Exception handling
# -----------------------------------------------------------------------------


class PandocMissing(ConversionException):
    """Exception raised when Pandoc is missing."""

    def __init__(self, *args, **kwargs):
        """Initialize the exception."""
        super().__init__(
            "Pandoc wasn't found.\n"
            "Please check that pandoc is installed:\n"
            "https://pandoc.org/installing.html"
        )


# -----------------------------------------------------------------------------
# Internal state management
# -----------------------------------------------------------------------------
def clean_cache():
    """Clean the internal cache."""
    global __version  # noqa
    __version = None


__version = None
