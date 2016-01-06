# Documenting nbconvert

[Documentation for `nbconvert`](https://nbconvert.readthedocs.org/en/latest/)
is hosted on ReadTheDocs.

## Build Documentation locally

1. Change directory to documentation root:

           $ cd docs

2. Install requirements:

           $ pip install -r requirements.txt

3. Build documentation using Makefile for Linux and OS X:

           $ make html

  or on Windows:

           $ make.bat html

4. Display the documentation locally by navigating to
   ``build/html/index.html`` in your browser:

   Or alternatively you may run a local server to display
   the docs. In Python 3:

           $ python -m http.server 8000

   In your browser, go to `http://localhost:8000`.

## Developing Documentation

### Helpful files and directories

* `conf.py` - Sphinx build configuration file
* `source` directory - source for documentation
* `source/api` directory - source files for generated API documentation
* `autogen_config.py` - Generates configuration of ipynb source files to rst
* `index.rst` - Main landing page of the Sphinx documentation
