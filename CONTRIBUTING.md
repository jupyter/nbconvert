# Contributing

We follow the
[Jupyter Contribution Workflow](https://jupyter.readthedocs.io/en/latest/contributing/content-contributor.html)
and the [IPython Contributing Guide](https://github.com/ipython/ipython/blob/master/CONTRIBUTING.md).

# Testing

In order to test all the features of nbconvert you need to have `pandoc` and
`TexLive` installed. 

In your environment `pip install -e '.[all]'` will be needed to be able to
run all of the tests and to test all of the features. 

If you only want to run some of the tests run `pip install -e '.[test]'`.

# Documentation

NbConvert includes a substantial amount of both user and API documentation. 

We use sphinx to build the API documentation. 

Much of the user documentation is written in Jupyter Notebooks and converted on the fly with nbsphinx. 


To build nbconvert's documentation you need to have `pandoc` and
`TexLive` installed. 

If you want to build the docs you will need to install the docs dependencies in addition to
the standard dependencies. You can get all of the dependencies by running `pip install -e
'.[all]'` and if you want only those needed to run the docs you can access them with `pip install -e '.[docs]'`.

Full build instructions can be found at [docs/README.md](docs/README.md).

# Releasing

If you are going to release a version of `nbconvert` you should also be capable
of testing it and building the docs. 

Please follow the instructions in [Testing](#testing) and [Documentation](#documentation) if
you are unfamiliar with how to do so.

The rest of the release process can be found in [these release instructions](./docs/source/development_release.rst).
