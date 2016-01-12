Executing notebooks
===================

.. module:: nbconvert.preprocessors

In this section we show how to execute a ``.ipynb`` notebook
document saving the result in notebook format.
To export the notebook to other formats see section
:doc:`nbconvert_library`.

Executing notebooks programmatically is useful, for example, as a test layer
in python libraries that include example notebooks, or as a way to
automate the data analysis in projects involving more than one notebook.

The same functionality of executing notebooks is exposed through a
:doc:`command line interface <usage>` or a python API interface.
In this section we will (mostly) illustrate how to use the python API interface.

A Quick example
---------------

Let's start with a complete quick example, leaving detailed explanations
to the following sections.

First we import nbconvert and the :class:`ExecutePreprocessor` class:

.. code-block:: python

    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor

Assuming that ``notebook_filename`` contains the path of a notebook,
we can load it with::

    with open(notebook_filename) as f:
        nb = nbformat.read(f, as_version=4)

Next, we configure the notebook execution mode::

    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

We specified two (optional) arguments ``timeout`` and ``kernel_name``, which
define respectively the execution timeout and the execution kernel.

    The option to specify **kernel_name** is new in nbconvert 4.2.
    When not specified or when using nbconvert <4.2,
    the default python kernel is chosen.

To actually run the notebook we call the method ``preprocess``::

    ep.preprocess(nb, {'metadata': {'path': 'notebooks/'}})

Hopefully, we will not get any errors during the notebook execution
(see the last section for error handling). Note that ``path`` specifies
in which folder to execute the notebook.
Finally, to save the resulting notebook::

    with open('executed_notebook.ipynb', 'wt') as f:
        nbformat.write(nb, f)

That's all. Your executed notebook will be saved in the current folder
in the file ``executed_notebook.ipynb``.

Execution arguments
-------------------

The arguments passed to :class:`ExecutePreprocessor` are configuration options
called `traitlets <http://traitlets.readthedocs.org/>`_.
There are many cool things about traitlets, for example
they enforce the type of the input and they can be accessed/modified as
class attributes. Moreover, each traitlet is automatically exposed
as command-line options. For example, we can pass the timeout from the
command-line like this::

    jupyter nbconvert --ExecutePreprocessor.timeout=600 --to notebook --execute mynotebook.ipynb

Let's now discuss in more detail the two traitlets we used.

The ``timeout`` traitlet defines the maximum time (in seconds) each notebook
cell is
allowed to run, if the execution takes longer an exception will be raised.
The default is 30 s, so in cases of long-running cells you may want to specify
an higher value.

The second traitlet, ``kernel_name``, allows specifying the name of the kernel
to be used for the execution. By default, the kernel name is obtained from the
notebook metadata. The traitlet ``kernel_name`` allows to specify a user-defined
kernel, overriding the value in the notebook metadata. A common use case
is that of a python 2/3 library which includes documentation/testing
notebooks. These notebooks will specify either a python2 or python3 kernel
in their metadata
(depending on the kernel used the last time the notebook was saved).
In reality, these notebooks will work on both python 2/3 and, for testing,
it is important to be able to execute them programmatically on both
versions. Here the traitlet ``kernel_name`` comes to help:
we can just run each notebook twice, specifying first "python2" and then
"python3" as kernel name.

Error Handling
--------------

In the previous sections we saw how to save an executed notebook, assuming
there are no execution error. But, what if there are errors?

An error during the notebook execution, by default, will stop the execution
and raise a ``CellExecutionError``. Conveniently, the source cell causing
the error and the original error name and message are also printed.
After an error, we can still save the notebook as before:

    with open('executed_notebook.ipynb', mode='wt') as f:
        nbformat.write(nb, f)

The saved notebook contains the output up until the failing cell,
and includes a full stack-trace and error (which can help debugging).
A useful pattern to execute notebooks while handling errors is the following::

    try:
        out = ep.preprocess(nb, {'metadata': {'path': run_path}})
    except CellExecutionError:
        msg = 'Error executing the notebook "%s".\n\n' % notebook_filename
        msg += 'See notebook "%s" for the traceback.' % notebook_filename_out
        print(msg)
        raise
    finally:
        nbformat.write(nb, open(notebook_filename_out, mode='wt'))

This will save the executed notebook regardless of execution errors.
In case of errors, however, an additional message is printed and the
``CellExecutionError`` is raised. The messages directs the user to
the saved notebook for further inspection.

As a last scenario, it is sometimes useful to execute notebooks which
raise exceptions, for example to show an error conditions.
In this case, instead of stopping the execution on the first error,
we can keep executing the notebook using the traitlet ``allow_errors``
(default False).
With ``allow_errors=True``,
the notebook is executed until the end, regardless of any error encountered
during the execution. The output notebook,
will contain the stack-traces and error messages for **all** the cells
raising exceptions.
