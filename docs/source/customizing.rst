
Customizing nbconvert
=====================

Under the hood, nbconvert uses `Jinja
templates <http://jinja2.readthedocs.org/en/latest/intro.html>`__ to
specify how the notebooks should be formatted. These templates can be
fully customized, allowing you to use nbconvert to create notebooks in
different formats with different styles as well.

Out of the box, nbconvert can be used to convert notebooks to plain
Python files. For example, the following command converts the
``example.ipynb`` notebook to Python and prints out the result:

.. code:: python

    %%bash
    
    jupyter nbconvert --to python 'example.ipynb' --stdout

From the code, you can see that non-code cells are also exported. As
mentioned above, if you want to change this behavior, you can use a
custom template. The custom template inherits from the Python template
and overwrites the markdown blocks so that they are empty.

Below is an example of a custom template, which we write to a file
called ``simplepython.tpl``. This template removes markdown cells from
the output, and also changes how the execution count numbers are
formatted:

.. code:: python

    %%writefile simplepython.tpl
    
    {% extends 'python.tpl'%}
    
    ## remove markdown cells
    {% block markdowncell -%}
    {% endblock markdowncell %}
    
    ## change the appearance of execution count
    {% block in_prompt %}
    # This was input cell with execution count: {{ cell.execution_count if cell.execution_count else ' ' }}
    {%- endblock in_prompt %}

Using this template, we see that the resulting Python code does not
contain anything that was previously in a markdown cell, and has special
comments regarding the execution counts:

.. code:: python

    %%bash
    
    jupyter nbconvert --to python 'example.ipynb' --stdout --template=simplepython.tpl

**See also**: `Template structure <_static/template_structure.html>`__,
for the available blocks you can override in your own templates.

A few gotchas
~~~~~~~~~~~~~

Jinja blocks use ``{% %}`` by default which does not play nicely with
LaTeX, hence thoses are replaced by ``((* *))`` in LaTeX templates.

Templates that use cell metadata
--------------------------------

The notebook file format supports attaching arbitrary JSON metadata to
each cell. Here, as an exercise, you will use the metadata to tag cells.

First you need to choose another notebook you want to convert to html,
and tag some of the cells with metadata. You can refer to the file
``soln/celldiff.js`` as an example or follow the Javascript tutorial to
figure out how do change cell metadata. Assuming you have a notebook
with some of the cells tagged as ``'Easy'``, ``'Medium'``, ``'Hard'``,
or ``<None>``, the notebook can be converted specially using a custom
template. Design your template in the cells provided below.

Hint: if your tags are located at ``cell.metadata.example.difficulty``,
the following Python code would get the value of the tag:
``cell['metadata'].get('example', {}).get('difficulty', '')``

The following **unorganized** lines of code may be a helpful starting
point:

.. code:: python

    %%writefile mytemplate.tpl
    
    {% extends 'html_full.tpl'%}
    {% block any_cell %}
    {{ super() }}
    <div style="background-color:red">
    <div style='background-color:orange'>

Once you have tagged the cells appropriately and written your template
using the cell above, try converting your notebook using the following
command:

.. code:: python

    %%bash
    
    jupyter nbconvert --to html <your chosen notebook.ipynb> --template=mytemplate.tpl
