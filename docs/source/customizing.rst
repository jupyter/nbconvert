
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

Template structure
------------------

Nbconvert templates consist of a set of nested blocks. When defining a
new template, you extend an existing template by overriding some of the
blocks.

All the templates shipped in nbconvert have the basic structure
described here, though some may define additional blocks.

.. code:: python

    from IPython.display import HTML, display
    with open('template_structure.html') as f:
        display(HTML(f.read()))



.. raw:: html

    <!--
    This is an HTML fragment that gets included into a notebook & rst document
    -->
    <style type="text/css">
    /* Overrides of notebook CSS for static HTML export */
    .jp-tpl-structure {
        font-family: sans;
    }
    
    .template_block {
        background-color: hsla(120, 60%, 70%, 0.2);
        margin: 10px;
        padding: 5px;
        border: 1px solid hsla(120, 60%, 70%, 0.5);
        border-left: 2px solid black;
    }
    
    .template_block:hover {
        border-color: black;
    }
    
    .template_block pre {
        background: transparent;
        padding: 0;
    }
    
    .big_vertical_ellipsis {
        font-size: 24pt;
    }
    
    </style>
    
    <div class='jp-tpl-structure'>
    <h3>Main page</h3>
    <div class="template_block">header</div>
    
    <div class="template_block">body
        <div class="template_block">any_cell
            <div class="template_block">codecell
                <div class="template_block">input_group
                    <div class="template_block">in_prompt</div>
                    <div class="template_block">input</div>
                </div>
                <div class="template_block">output_group
                    <div class="template_block">output_prompt</div>
                    <div class="template_block">outputs (see below)</div>
                </div>
            </div>
        </div>
        <div class="template_block">any_cell
            <div class="template_block">markdowncell</div>
        </div>
        <div class="template_block">any_cell
            <div class="template_block">rawcell</div>
        </div>
        <div class="template_block">any_cell
            <div class="template_block">unknowncell</div>
        </div>
        <div class="big_vertical_ellipsis">⋮</div>
    </div>
    
    <div class="template_block">footer</div>
    
    <h3>Outputs</h3>
    
    <div class="template_block">outputs
        <div class="template_block">output
            <div class="template_block">execute_result</div>
        </div>
        <div class="template_block">output
            <div class="template_block">stream_stdout</div>
        </div>
        <div class="template_block">output
            <div class="template_block">stream_stderr</div>
        </div>
        <div class="template_block">output
            <div class="template_block">display_data
                <div class="template_block">data_priority
                    <div class="template_block">data_pdf / data_svg / data_png /
                        data_html / data_markdown / data_jpg / data_text /
                        data_latex / data_javascript / data_other
                    </div>
                </div>
            </div>
        </div>
        <div class="template_block">output
            <div class="template_block">error
                <div class="template_block">traceback_line</div>
                <div class="big_vertical_ellipsis">⋮</div>
            </div>
        </div>
        <div class="big_vertical_ellipsis">⋮</div>
    </div>
    
    <h3>Extra HTML blocks (full.tpl)</h3>
    <div class="template_block">header
        <pre>&lt;head&gt;</pre>
        <div class="template_block">html_head</div>
        <pre>&lt;/head&gt;</pre>
    </div>
    
    <h3>Extra Latex blocks</h3>
    <div class="template_block">header
        <div class="template_block">docclass</div>
        <div class="template_block">packages</div>
        <div class="template_block">definitions
            <div class="template_block">title</div>
            <div class="template_block">date</div>
            <div class="template_block">author</div>
        </div>
        <div class="template_block">commands
            <div class="template_block">margins</div>
        </div>
    </div>
    <div class="template_block">body
        <div class="template_block">predoc
            <div class="template_block">maketitle</div>
            <div class="template_block">abstract</div>
        </div>
        ... other fields as above ...
        <div class="template_block">postdoc
            <div class="template_block">bibliography</div>
        </div>
    </div>
    </div>
    



A few gotchas
~~~~~~~~~~~~~

Jinja blocks use ``{% %}`` by default which does not play nicely with
LaTeX, so those are replaced by ``((* *))`` in LaTeX templates.

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

.. code:: python

    cell['metadata'].get('example', {}).get('difficulty', '')

The following lines of code may be a helpful starting point:

.. code:: python

    %%writefile mytemplate.tpl
    
    {% extends 'full.tpl'%}
    {% block any_cell %}
        <div style="border:thin solid red">
            {{ super() }}
        </div>
    {% endblock any_cell %}

Once you have tagged the cells appropriately and written your template
using the cell above, try converting your notebook using the following
command:

.. code:: python

    %%bash
    
    jupyter nbconvert --to html <your chosen notebook.ipynb> --template=mytemplate.tpl
