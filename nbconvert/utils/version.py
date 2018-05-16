# encoding: utf-8
"""
Utilities for version comparison

It is a bit ridiculous that we need these.
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from distutils.version import LooseVersion


def check_version(v, min_v, max_v):
    """check version string v >= min_v and v < max_v

    Parameters
    ----------
    v : str
        version of the package
    min_v : str
        minimal version supported
    max_v : str
        earliest version not supported

    Note: If dev/prerelease tags result in TypeError for string-number
    comparison, it is assumed that the check passes and the version dependency
    is satisfied. Users on dev branches are responsible for keeping their own
    packages up to date.
    """

    try:
        return LooseVersion(v) >= LooseVersion(min_v) and LooseVersion(v) < LooseVersion(max_v)
    except TypeError:
        return True

