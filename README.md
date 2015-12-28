# Jupyter Notebook Conversion, nbconvert

`jupyter nbconvert` converts notebooks to various other formats via [Jinja][] templates.
The nbconvert tool allows you to convert an `.ipynb` notebook document file
into various static formats including:
* HTML
* LaTEX
* PDF
* Reveal JS
* Markdown (md)
* ReStructured Text (rst)
* executable script.

## Usage

From the command line, use nbconvert to convert a Jupyter notebook (**input**) to a
a different format (**output**). The basic command structure is:

    $ jupyter nbconvert --to <output format> <input notebook>

where *<output format>* is the desired output format and *<input notebook>* is the
filename of the Jupyter notebook.

### Example: Convert a notebook to HTML

Convert Juptyer notebook `mynotebook.ipynb` file to HTML using:

   $ jupyter nbconvert --to html mynotebook.ipynb

This command creates an HTML output file named `mynotebook.html`.

## Resources

- [Project Jupyter website](https://jupyter.org)
- [Online Demo at try.jupyter.org](https://try.jupyter.org)
- [Documentation for Jupyter nbconvert](https://nbconvert.readthedocs.org/en/latest/)
  [[PDF](https://media.readthedocs.org/pdf/nbconvert/latest/nbconvert.pdf)]
- [Documentation for Project Jupyter](https://jupyter.readthedocs.org/en/latest/index.html)
  [[PDF](https://media.readthedocs.org/pdf/jupyter/latest/jupyter.pdf)]
- [Issues](https://github.com/jupyter/nbconvert/issues)
- [Technical support - Jupyter Google Group](https://groups.google.com/forum/#!forum/jupyter)


[Jinja]: http://jinja.pocoo.org/