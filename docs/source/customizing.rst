
Customizing nbconvert
=====================

Look at the first 20 lines of the ``python`` exporter

.. code:: python

    pyfile = !jupyter nbconvert --to python 'Index.ipynb' --stdout
    for l in pyfile[20:40]:
        print l

From the code, you can see that non-code cells are also exported. If you
want to change this behavior, you can use a custom template. The custom
template inherits from the Python template and overwrites the markdown
blocks so that they are empty.

.. code:: python

    %%writefile simplepython.tpl
    {% extends 'python.tpl'%}
    
    {% block markdowncell -%}
    {% endblock markdowncell %}
    
    ## we also want to get rig of header cell
    {% block headingcell -%}
    {% endblock headingcell %}
    
    ## and let's change the appearance of input prompt
    {% block in_prompt %}
    # This was input cell with prompt number : {{ cell.prompt_number if cell.prompt_number else ' ' }}
    {%- endblock in_prompt %}

.. code:: python

    pyfile = !jupyter nbconvert --to python 'Index.ipynb' --stdout --template=simplepython.tpl
    
    for l in pyfile[4:40]:
        print l
    print '...'

For details about the template syntax, refer to `Jinja's
manual <http://jinja2.readthedocs.org/en/latest/intro.html>`__.

Template that use cells metadata
--------------------------------

The notebook file format supports attaching arbitrary JSON metadata to
each cell. Here, as an exercise, you will use the metadata to tags
cells.

First you need to choose another notebook you want to convert to html,
and tag some of the cells with metadata. You can refere to the file
``soln/celldiff.js`` as an example or follow the Javascript tutorial to
figure out how do change cell metadata. Assuming you have a notebook
with some of the cells tagged as
``Easy``\ \|\ ``Medium``\ \|\ ``Hard``\ \|\ ``<None>``, the notebook can
be converted specially using a custom template. Design your template in
the cells provided below.

The following, unorganized lines of code, may be of help:

::

    {% extends 'html_full.tpl'%}
    {% block any_cell %}
    {{ super() }}
    <div style="background-color:red">
    <div style='background-color:orange'>

If your key name under ``cell.metadata.example.difficulty``, the
following code would get the value of it:

``cell['metadata'].get('example',{}).get('difficulty','')``

Tip: Use ``%%writefile`` to edit the template in the notebook.

.. code:: python

    %%bash
    # jupyter nbconvert --to html <your chosen notebook.ipynb> --template=<your template file>

.. code:: python

    %loadpy soln/coloreddiff.tpl

.. code:: python

    # jupyter nbconvert --to html '04 - Custom Display Logic.ipynb' --template=soln/coloreddiff.tpl
