.. highlight:: none

Dejavu
======

Dejavu intends to be a tool to facilitate for Jupyter users to generate static outputs from their notebooks, mimicking the behavior of `voilà <https://github.com/voila-dashboards/voila>`_.

Running dejavu
--------------

Dejavu works exactly the same as nbconvert and you can use all command line options that you would with nbconvert. To run a default instance::

    jupyter dejavu notebook.ipynb

In case you want to show code in adition to its output use the flag ``--show-input``.


Configuring the Notebook for slides presentations
-------------------------------------------------

In case the user intends to do a slide presentation out of their Jupyter notebook it's recommended to use the ``reveal`` template. In orders to obtain a better result from it's advised to use the slides metadatas available in the cells:


* In the notebook, select a cell and click on the "Property Inspector menu"

.. tip::

   The "Property Inspector menu" can be located in the right side bar, its symbol contains two gears.

* Select a cell in the notebook

* In the Property Inspector menu select the cell's slide type:

    * Slide
    * Sub-Slide
    * Fragment
    * Skip
    * Notes

* Repeat the process for all cells
