Installation
============

.. seealso::

   `Installing Jupyter <https://jupyter.readthedocs.org/en/latest/install.html>`__
     Nbconvert is part of the Jupyter ecosystem.

Installing nbconvert
--------------------

Nbconvert is packaged for both pip and conda, so you can install it with::

    pip install nbconvert
    # OR
    conda install nbconvert

If you're new to Python, we recommend installing `Anaconda <https://www.continuum.io/downloads>`_,
a Python distribution which includes nbconvert and the other Jupyter components.

Installing Pandoc
-----------------

For converting markdown to formats other than HTML, nbconvert uses
`Pandoc <http://pandoc.org>`_ (1.12.1 or later).

To install pandoc on Linux, you can generally use your package manager::

    sudo apt-get install pandoc

On other platforms, you can get pandoc from
`their website <http://pandoc.org/installing.html>`_.
