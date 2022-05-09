"""A build backend that handles installing the template files.

See https://peps.python.org/pep-0517/#in-tree-build-backends
"""
import os
import sys
from urllib.request import urlopen

from flit_core.buildapi import build_editable  # noqa
from flit_core.buildapi import build_sdist  # noqa
from flit_core.buildapi import build_wheel  # noqa
from flit_core.buildapi import (
    get_requires_for_build_editable as get_requires_for_build_editable_orig,
)
from flit_core.buildapi import (
    get_requires_for_build_sdist as get_requires_for_build_sdist_orig,
)
from flit_core.buildapi import (
    get_requires_for_build_wheel as get_requires_for_build_wheel_orig,
)

notebook_css_version = "5.4.0"
notebook_css_url = "https://cdn.jupyter.org/notebook/%s/style/style.min.css" % notebook_css_version

jupyterlab_css_version = "3.1.11"
jupyterlab_css_url = (
    "https://unpkg.com/@jupyterlab/nbconvert-css@%s/style/index.css" % jupyterlab_css_version
)

jupyterlab_theme_light_version = "3.1.11"
jupyterlab_theme_light_url = (
    "https://unpkg.com/@jupyterlab/theme-light-extension@%s/style/variables.css"
    % jupyterlab_theme_light_version
)

jupyterlab_theme_dark_version = "3.1.11"
jupyterlab_theme_dark_url = (
    "https://unpkg.com/@jupyterlab/theme-dark-extension@%s/style/variables.css"
    % jupyterlab_theme_dark_version
)

template_css_urls = {
    "lab": [
        (jupyterlab_css_url, "index.css"),
        (jupyterlab_theme_light_url, "theme-light.css"),
        (jupyterlab_theme_dark_url, "theme-dark.css"),
    ],
    "classic": [(notebook_css_url, "style.css")],
}

osp = os.path
here = osp.abspath(osp.dirname(__file__))
templates_dir = osp.join(here, "jupyter-data", "share", "jupyter", "nbconvert", "templates")


def _get_css_file(template_name, url, filename):
    """Get a css file and download it to the templates dir"""
    directory = osp.join(templates_dir, template_name, "static")
    dest = osp.join(directory, filename)
    if not osp.exists(directory):
        os.makedirs(directory)
    print("Downloading CSS: %s" % url)
    try:
        css = urlopen(url).read()
    except Exception as e:
        msg = f"Failed to download css from {url}: {e}"
        print(msg, file=sys.stderr)
        if osp.exists(dest):
            print("Already have CSS: %s, moving on." % dest)
        else:
            raise OSError("Need CSS to proceed.")
        return

    with open(dest, "wb") as f:
        f.write(css)
    print("Downloaded Notebook CSS to %s" % dest)


def _get_css_files():
    """Get all of the css files if necessary"""
    in_checkout = osp.exists(osp.abspath(osp.join(here, "..", ".git")))
    if in_checkout:
        print("Not running from git, nothing to do")
        return

    for template_name, resources in template_css_urls.items():
        for url, filename in resources:
            _get_css_file(template_name, url, filename)


def get_requires_for_build_wheel(config_settings=None):
    _get_css_files()
    return get_requires_for_build_wheel_orig(config_settings=config_settings)


def get_requires_for_build_sdist(config_settings=None):
    _get_css_files()
    return get_requires_for_build_sdist_orig(config_settings=config_settings)


def get_requires_for_build_editable(config_settings=None):
    _get_css_files()
    return get_requires_for_build_editable_orig(config_settings=config_settings)
