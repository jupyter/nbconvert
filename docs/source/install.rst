.. highlight:: none

Installation
============

.. seealso::

   `Installing Jupyter <https://jupyter.readthedocs.io/en/latest/install.html>`__
     Nbconvert is part of the Jupyter ecosystem.

Supported Python versions
-------------------------

Currently Python 3.6-3.8 is supported and tested by nbconvert.

However, nbconvert 6.0 provides limited support for Python 3.6. nbconvert 6.1 will drop
support for Python 3.6. Limited support means we will test and run CI on Python 3.6.12
or higher. Issues that are found only affecting Python 3.6 are not guaranteed to be
fixed. We recommend all users of nbconvert use Python 3.7 and higher.

Installing nbconvert
--------------------

Nbconvert is packaged for both pip and conda, so you can install it with::

    pip install nbconvert

    # OR

    conda install nbconvert

The `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ and `Miniforge <https://github.com/conda-forge/miniforge/>`_ distributions both provide a minimal conda installation.

.. important::

    To unlock its full capabilities, nbconvert requires Pandoc, TeX
    (specifically, XeLaTeX) and Pyppeteer. These must be installed separately.

Installing Pandoc
-----------------

For converting markdown to formats other than HTML, nbconvert uses
`Pandoc <https://pandoc.org>`_ (1.12.1 or later).

To install pandoc on Linux, you can generally use your package manager::

    sudo apt-get install pandoc

On other platforms, you can get pandoc from
`their website <https://pandoc.org/installing.html>`_.

Installing TeX
--------------

For converting notebooks to PDF (with ``--to pdf``), nbconvert makes use of LaTeX
and the XeTeX as the rendering engine.

.. versionadded:: 5.0

    We use XeTeX as the rendering engine rather than pdfTeX (as
    in earlier versions). XeTeX can access fonts through native
    operating system libraries, it has better support for OpenType
    formatted fonts and Unicode characters.

To install a complete TeX environment (including XeLaTeX and
the necessary supporting packages) by hand can be tricky.
Fortunately, there are packages that make this much easier. These
packages are specific to different operating systems:

* Linux: `TeX Live <http://tug.org/texlive/>`_

  * E.g. on Debian or Ubuntu::

        sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-generic-recommended

* macOS (OS X): `MacTeX <http://tug.org/mactex/>`_.
* Windows: `MikTex <https://miktex.org/>`_

Because nbconvert depends on packages and fonts included in standard
TeX distributions, if you do not have a complete installation, you
may not be able to use nbconvert's standard tooling to convert
notebooks to PDF.

Installing Chromium
-------------------

For converting notebooks to PDF with ``--to webpdf``, nbconvert requires the
`Pyppeteer <https://github.com/pyppeteer/pyppeteer>`_ Chromium automation library.

Pyppeteer makes use of a specific version of Chromium. If it does not find a suitable
installation of the web browser, it can automatically download it if the ``--allow-chromium-download``
flag is passed to the command line.

To install a suitable version of pyppeteer, you can pip install ``nbconvert[webpdf]``.

PDF conversion on a limited TeX environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are only able to install a limited TeX environment, there are two main routes you could take to convert to PDF:

1. Using TeX by hand
    a. You could convert to ``.tex`` directly; this requires Pandoc.
    b. edit the file to accord with your local environment
    c. run ``xelatex`` directly.
2. Custom exporter
    a. You could write a :ref:`custom exporter <external_exporters>`
       that takes your system's limitations into account.
