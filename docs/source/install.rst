Installation
============

.. seealso::

   `Installing Jupyter <https://jupyter.readthedocs.io/en/latest/install.html>`__
     Nbconvert is part of the Jupyter ecosystem.

Installing nbconvert
--------------------

Nbconvert is packaged for both pip and conda, so you can install it with::

    pip install nbconvert
    # OR
    conda install nbconvert

If you're new to Python, we recommend installing `Anaconda <https://www.continuum.io/downloads>`_,
a Python distribution which includes nbconvert and the other Jupyter components.

.. important::
    
    To unlock nbconvert's full capabilities requires Pandoc and TeX 
    (specifically, XeLaTeX). These must be installed separately.

Installing Pandoc
-----------------

For converting markdown to formats other than HTML, nbconvert uses
`Pandoc <http://pandoc.org>`_ (1.12.1 or later).

To install pandoc on Linux, you can generally use your package manager::

    sudo apt-get install pandoc

On other platforms, you can get pandoc from
`their website <http://pandoc.org/installing.html>`_.

Installing TeX
--------------

For converting to PDF, nbconvert uses the TeX document preparation 
ecosystem. It produces an intermediate ``.tex`` file which is 
compiled by the XeTeX engine with the LaTeX2e format (via the 
``xelatex`` command) to produce PDF output. 

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
* macOS (OS X): `MacTeX <http://tug.org/mactex/>`_.
* Windows: `MikTex <http://www.miktex.org/>`_

Because nbconvert depends on packages and fonts included in standard 
TeX distributions, if you do not have a complete installation, you 
may not be able to use nbconvert's standard tooling to convert 
notebooks to PDF. 

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
