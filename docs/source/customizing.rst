Creating Custom Templates for nbconvert
=======================================

Selecting a template
--------------------

Most exporters in nbconvert are subclasses of `TemplateExporter`, and make use of
jinja to render notebooks into the destination format.

Alternative nbconvert templates can be selected by name from the command line with the
``--template`` option. For example, to use the ``reveal`` template with the HTML exporter,
one can type.

.. sourcecode:: bash

   jupyter nbconvert <path-to-notebook> --to html --template reveal

Where are nbconvert templates installed?
----------------------------------------

Nbconvert templates are *directories* containing resources for nbconvert template
exporters such as jinja templates and associated assets. They are installed in the
**data directory** of nbconvert, namely ``<installation prefix>/share/jupyter/nbconvert``.
Nbconvert includes several templates already.

For example, three HTML templates are provided in nbconvert core for the HTML exporter:

 - ``lab`` (The default HTML template, which produces the same DOM structure as JupyterLab)
 - ``classic`` (The HTML template styled after the classic notebook)
 - ``reveal`` (For producing slideshows).

.. note::

    Running ``jupyter --paths`` will show all Jupyter directories and search paths.

    For example, on Linux, ``jupyter --paths`` returns:

    .. code::

        $ jupyter --paths
        config:
            /home/<username>/.jupyter
            /<sys-prefix>/etc/jupyter
            /usr/local/etc/jupyter
            /etc/jupyter
        data:
            /home/<username>/.local/share/jupyter
            /<sys-prefix>/share/jupyter
            /usr/local/share/jupyter
            /usr/share/jupyter
        runtime:
            /home/<username>/.local/share/jupyter/runtime


Adding Additional Template Paths
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to add additional paths to be searched, you need to pass ``TemplateExporter.extra_template_basedirs``
config options indicating the extra directories to search for templates. Be careful not to override
``TemplateExporter.template_paths`` unless you intend to replace ALL paths and don't want the default
locations included.

When using the commandline the extra template paths are added by calling
``--TemplateExporter.extra_template_basedirs=path/you/want/included``.


The content of nbconvert templates
----------------------------------

conf.json
~~~~~~~~~

Nbconvert templates all include a ``conf.json`` file at the root of the directory,
which is used to indicate

 - the base template that it is inheriting from.
 - the mimetypes of the template.
 - preprocessors classes to register in the exporter when using that template.

Inspecting the configuration of the reveal template we see that it inherits from the lab
template, exports text/html, and enables two preprocessors called "100-pygments" and "500-reveal".

.. code::

    {
      "base_template": "lab",
      "mimetypes": {
        "text/html": true
      },
      "preprocessors": {
        "100-pygments": {
            "type": "nbconvert.preprocessors.CSSHTMLHeaderPreprocessor",
            "enabled": true
        },
        "500-reveal": {
          "type": "nbconvert.exporters.slides._RevealMetadataPreprocessor",
          "enabled": true
        }
      }
    }

Inheritance
~~~~~~~~~~~

Nbconvert walks up the inheritance structure determined by ``conf.json`` and produces an agregated
configuration, merging the dictionaries of registered preprocessors.
The lexical ordering of the preprocessors by name determines the order in which they will be run.

Besides the ``conf.json`` file, nbconvert templates most typically include jinja templates files,
although any other resource from the base template can be overriden in the derived template.

For example, inspecting the content of the ``classic`` template located in
``share/jupyter/nbconvert/templates/classic``, we find the following content:

.. code::

    share/jupyter/nbconvert/templates/classic
    ├── static
    │   └── styles.css
    ├── conf.json
    ├── index.html.j2
    └── base.html.j2

The ``classic`` template exporter includes a ``index.html.j2`` jinja template (which is the main entry point
for HTML exporters) as well as CSS and a base template file in ``base.html.j2``.

.. note::

   A template inheriting from ``classic`` would specify ``"base_template": "classic"`` and could
   override any of these files. For example, one could make a "classiker" template merely providing
   an alternative ``styles.css`` file.

Inheritance in Jinja
~~~~~~~~~~~~~~~~~~~~

In nbconvert, jinja templates can inherrit from any other jinja template available in its current directory
or base template directory by name. Jinja templates of other directories can be addressed by their relative path
from the Jupyter data directory.

For example, in the reveal template, ``index.html.j2`` extends ``base.html.j2`` which is in the same directory, and
``base.html.j2`` extends ``lab/base.html.j2``. This approach allows using content that is available in other templates
or may be overriden in the current template.
