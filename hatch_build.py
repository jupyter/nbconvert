"""Custom build script for hatch backend"""

import io
import os
import sys
import zipfile
from urllib.request import urlopen

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

# The origin server behind cdn.jupyter.org is gone, so the notebook 5.4.0 stylesheet comes from the
# wheel that ships it; the bytes match what the CDN served.
notebook_css_url = (
    "https://files.pythonhosted.org/packages/d0/ca/a5a5ac9c839868ceddaa2672c399492ac1dbd4c4ce68f833a72a619fc225/"
    "notebook-5.4.0-py2.py3-none-any.whl"
)
notebook_css_member = "notebook/static/style/style.min.css"

jupyterlab_css_version = "4.0.2"
jupyterlab_css_url = (
    "https://unpkg.com/@jupyterlab/nbconvert-css@%s/style/index.css" % jupyterlab_css_version
)

jupyterlab_theme_light_version = "4.0.2"
jupyterlab_theme_light_url = (
    "https://unpkg.com/@jupyterlab/theme-light-extension@%s/style/variables.css"
    % jupyterlab_theme_light_version
)

jupyterlab_theme_dark_version = "4.0.2"
jupyterlab_theme_dark_url = (
    "https://unpkg.com/@jupyterlab/theme-dark-extension@%s/style/variables.css"
    % jupyterlab_theme_dark_version
)

template_css_urls = {
    "lab": [
        (jupyterlab_css_url, "index.css", None),
        (jupyterlab_theme_light_url, "theme-light.css", None),
        (jupyterlab_theme_dark_url, "theme-dark.css", None),
    ],
    "classic": [(notebook_css_url, "style.css", notebook_css_member)],
}

osp = os.path
here = osp.abspath(osp.dirname(__file__))
templates_dir = osp.join(here, "share", "templates")


def _get_css_file(template_name, url, filename, member):
    """Get a css file and download it to the templates dir, from inside the zip at url if member is set"""
    directory = osp.join(templates_dir, template_name, "static")
    dest = osp.join(directory, filename)
    if osp.exists(dest):
        print("Already have CSS: %s, moving on." % dest)
        return
    if not osp.exists(directory):
        os.makedirs(directory)
    print("Downloading CSS: %s" % url)
    try:
        css = urlopen(url).read()  # noqa: S310
        if member:
            css = zipfile.ZipFile(io.BytesIO(css)).read(member)
    except Exception as e:
        msg = f"Failed to download css from {url}: {e}"
        print(msg, file=sys.stderr)
        msg = "Need CSS to proceed."
        raise OSError(msg) from None
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
        for url, filename, member in resources:
            _get_css_file(template_name, url, filename, member)


class CustomHook(BuildHookInterface):
    """A custom build hook for nbconvert."""

    def initialize(self, version, build_data):
        """Initialize the hook."""
        if self.target_name not in ["wheel", "sdist"]:
            return
        _get_css_files()
