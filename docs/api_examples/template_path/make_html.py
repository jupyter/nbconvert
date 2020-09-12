"""
this script builds html files with either classic or classic_clone templates

Note: nbconvert 6.0 changed ``template_path`` to ``template_paths``
"""
import nbformat
from traitlets.config import Config
from nbconvert import HTMLExporter

nbfile = "quiz_notebook.ipynb"
the_ipynb = nbformat.read(nbfile, as_version=4)

c = Config()
c.TemplateExporter.template_paths = ['.', './project_templates']
for template in ['classic', 'classic_clone']:
    c.HTMLExporter.template_name = template
    html_exporter = HTMLExporter(config=c)
    (body, resources) = html_exporter.from_notebook_node(the_ipynb)
    with open(f"{template}.html", 'w') as outfile:
        outfile.write(body)
    print(f"\n{'*'*20}\n{template} succeeds\n{'*'*20}\n")
