# Contributing

We follow the
[Jupyter Contribution Workflow](https://jupyter.readthedocs.io/en/latest/contributor/content-contributor.html)
and the [IPython Contributing Guide](https://github.com/ipython/ipython/blob/master/CONTRIBUTING.md).

# Testing

In order to test all the features of nbconvert you need to have `pandoc` and
`TexLive` installed. 

In your environment `pip install nbconvert[all]` will be needed to be able to
run all of the tests and to test all of the features. 

If you only want to run some of the tests run `pip install nbconvert[test]`.

# Releasing

If you are going to release a version of `nbconvert` you should also be capable
of testing it. Please follow the instructions in [Testing](#testing).
