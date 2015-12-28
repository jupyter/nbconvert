# Documenting nbconvert

[Documentation for `nbconvert`](https://nbconvert.readthedocs.org/en/latest/)
is hosted on ReadTheDocs.

## Build Documentation locally

0. Change directory to documentation root:

    $ cd docs

1. Install requirements:

    $ pip install -r requirements.txt

2. Build documentation using Makefile for Linux and OS X:

    $ make html

or for Windows:

    $ make.bat html

3. Display the documentation locally:

    $ open build/html/index.html

Or alternatively you may run a local server to display the docs. In Python 3:

    $ python -m http.server 8000

In your browser, go to `http://localhost:8000`

## Developing Documentation

### Helpful files and directories

* conf.py - Sphinx build configuration file
* source directory - source for documentation
* source/api - source files for generated API documentation
* autogen_config.py - Generates configuration of ipynb source files to rst
* index.rst - Main landing page of the Sphinx documentation
