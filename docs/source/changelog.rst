.. _changelog:

====================
Changes in nbconvert
====================

5.3.1
-----
`5.3.1 on Github <https://github.com/jupyter/nbconvert/milestones/5.3.1>`__

- MANIFEST.in updated to include ``LICENSE`` and ``scripts/`` when creating sdist. #666

5.3
---
`5.3 on Github <https://github.com/jupyter/nbconvert/milestones/5.3>`__

Major features
~~~~~~~~~~~~~~

Tag Based Element Filtering
+++++++++++++++++++++++++++

For removing individual elements from notebooks, we need a way to signal to
nbconvert that the elements should be removed. With this release, we introduce
the use of tags for that purpose.

Tags are user-defined strings attached to cells or outputs. They are stored in
cell or output metadata. For more on tags see the `nbformat docs on cell
metadata <http://nbformat.readthedocs.io/en/latest/format_description.html#cell-metadata>`__.

**Usage**: 

1. Apply tags to the elements that you want to remove. 
   
For removing an entire cell, the cell input, or all cell outputs apply the tag
to the cell. 

For removing individual outputs, put the tag in the output metadata
using a call like ``display(your_output_element, metadata={tags=[<your_tags_here>]})``. 

*NB*: Use different tags depending on whether you want to remove the entire cell, the input, all outputs, or individual outputs.

2. Add the tags for removing the different kinds of elements to the following
   traitlets. Which kind of element you want to remove determines which
   traitlet you add the tags to.

The following traitlets remove elements of different kinds: 

- ``remove_cell_tags``: removes cells 
- ``remove_input_tags``: removes inputs
- ``remove_all_outputs_tag``: removes all outputs  
- ``remove_single_output_tag``: removes individual outputs

Comprehensive notes
~~~~~~~~~~~~~~~~~~~

- new: configurable ``browser`` in ServePostProcessor :ghpull:`618`
- new: ``--clear-output`` command line flag to clear output in-place :ghpull:`619`
- new: remove elements based on tags with ``TagRemovePreprocessor``. :ghpull:`640`, :ghpull:`643`
- new: CellExecutionError can now be imported from ``nbconvert.preprocessors`` :ghpull:`656`
- new: slides now can enable scrolling and custom transitions :ghpull:`600`

- docs: Release instructions for nbviewer-deploy
- docs: improved instructions for handling errors using the ``ExecutePreprocessor`` :ghpull:`656`

- tests: better height/width metadata testing for images in rst & html :ghpull:`601` :ghpull:`602`
- tests: normalise base64 output data to avoid false positives :ghpull:`650`
- tests: normalise ipython traceback messages to handle old and new style :ghpull:`631`

- bug: mathjax obeys ``\\(\\)`` & ``\\[\\]`` (both nbconvert & pandoc) :ghpull:`609` :ghpull:`617`
- bug: specify default templates using extensions :ghpull:`639`
- bug: fix pandoc version number :ghpull:`638`
- bug: require recent mistune version :ghpull:`630`
- bug: catch errors from IPython ``execute_reply`` and ``error`` messages :ghpull:`642`

- nose completely removed & dependency dropped :ghpull:`595` :ghpull:`660`
- mathjax processing in mistune now only uses inline grammar :ghpull:`611`
- removeRegex now enabled by default on all TemplateExporters, does not remove cells with outputs :ghpull:`616`
- validate notebook after applying each preprocessor (allowing additional attributes) :ghpull:`645`
- changed COPYING.md to LICENSE for more standard licensing that GitHub knows how to read :ghpull:`654`

5.2.1
-----

`5.2 on GitHub <https://github.com/jupyter/nbconvert/milestones/5.2>`__

Major features
~~~~~~~~~~~~~~

In this release (along with the usual bugfixes and documentation improvements,
which are legion) we have a few new major features that have been requested for
a long time:

Global Content Filtering
++++++++++++++++++++++++

You now have the ability to remove input or output from code cells, markdown
cells and the input and output prompts. The easiest way to access all of these
is by using traitlets like TemplateExporter.exclude_input = True (or, for
example HTMLExporter.exclude_markdown = True if you wanted to make it specific
to HTML output). On the command line if you just want to not have input or
output prompts just use --no-prompt.

Execute notebooks from a function
+++++++++++++++++++++++++++++++++

You can now use the executenb function to execute notebooks as though you ran
the execute preprocessor on the notebooks. It returns the standard notebook and
resources options.

Remove cells based on regex pattern
+++++++++++++++++++++++++++++++++++

This removes cells based on their matching a regex pattern (by default, empty
cells). This is the RegexRemovePreprocessor.

Script exporter entrypoints for nonpython scripts
+++++++++++++++++++++++++++++++++++++++++++++++++

Now there is an entrypoint for having an exporter specific to the type of script
that is being exported. While designed for use with the IRkernel in particular
(with a script exporter focused on exporting R scripts) other non-python kernels
that wish to have a language specific exporter can now surface that directly.

Comprehensive notes
~~~~~~~~~~~~~~~~~~~

- new: configurable ExecutePreprocessor.startup_timeout configurable :ghpull:`583`
- new: RemoveCell preprocessor based on cell content (defaults to empty cell) :ghpull:`575`
- new: function for executing notebooks: `executenb` :ghpull:`573`
- new: global filtering to remove inputs, outputs, markdown cells (&c.), this works on all templates :ghpull:`554`
- new: script exporter entrypoint :ghpull:`531`
- new: configurable anchor link text (previously ¶) `HTMLExporter.anchor_link_text` :ghpull:`522`

- new: configurable values for slides exporter :ghpull:`542` :ghpull:`558`

- improved releases (how-to documentation, version-number generation and checking) :ghpull:`593`
- doc improvements  :ghpull:`593` :ghpull:`580` :ghpull:`565` :ghpull:`554`
- language information from cell magics (for highlighting) is now included in more formats :ghpull:`586`
- mathjax upgrades and cdn fixes :ghpull:`584` :ghpull:`567`
- better CI :ghpull:`571` :ghpull:`540`
- better traceback behaviour when execution errs :ghpull:`521`
- deprecated nose test features removed :ghpull:`519`

- bug fixed: we now respect width and height metadata on jpeg and png mimetype outputs :ghpull:`588`
- bug fixed: now we respect the `resolve_references` filter in `report.tplx` :ghpull:`577`
- bug fixed: output metadata now is removed by ClearOutputPreprocessor :ghpull:`569`
- bug fixed: display id respected in execute preproessor :ghpull:`563`
- bug fixed: dynamic defaults for optional jupyter_client import :ghpull:`559`
- bug fixed: don't self-close non-void HTML tags :ghpull:`548`
- buf fixed: upgrade jupyter_client dependency to 4.2 :ghpull:`539`
- bug fixed: LaTeX output through md→LaTeX conversion shouldn't be touched :ghpull:`535`
- bug fixed: now we escape `<` inside math formulas when converting to html :ghpull:`514`

Credits
~~~~~~~

This release has been larger than previous releases. In it 33 authors
contributed a total of 546 commits.

Many thanks to the following individuals who contributed to this release (in
alphabetical order):

- Adam Chainz
- Andreas Mueller
- Bartosz T
- Benjamin Ragan-Kelley
- Carol Willing
- Damián Avila
- Elliot Marsden
- Gao, Xiang
- Jaeho Shin
- Jan Schulz
- Jeremy Kun
- Jessica B. Hamrick
- John B Nelson
- juhasch
- Livia Barazzetti
- M Pacer
- Matej Urbas
- Matthias Bussonnier
- Matthias Geier
- Maximilian Albert
- Michael Scott Cuthbert
- Nicholas Bollweg
- Paul Gowder
- Paulo Villegas
- Peter Parente
- Philipp A
- Scott Sanderson
- Srinivas Reddy Thatiparthy
- Sylvain Corlay
- Thomas Kluyver
- Till Hoffmann
- Xiang Gao
- YuviPanda


5.1.1
-----

`5.1.1 on GitHub <https://github.com/jupyter/nbconvert/milestones/5.1.1>`__

- fix version numbering because of incomplete previous version number

5.1
---

`5.1 on GitHub <https://github.com/jupyter/nbconvert/milestones/5.1>`__

- improved CSS (specifically tables, in line with notebook) :ghpull:`498`
- improve in-memory templates handling :ghpull:`491`
- test improvements :ghpull:`516` :ghpull:`509` :ghpull:`505`
- new configuration option: IOPub timeout :ghpull:`513`
- doc improvements :ghpull:`489` :ghpull:`500` :ghpull:`493` :ghpull:`506`
- newly customizable: output prompt :ghpull:`500`
- more python2/3 compatibile unicode handling :ghpull:`502`

5.0
---

`5.0 on GitHub <https://github.com/jupyter/nbconvert/milestones/5.0>`__

- Use :command:`xelatex` by default for latex export, improving unicode and font support.
- Use entrypoints internally to access Exporters, allowing for packages to declare custom exporters more easily.
- New ASCIIDoc Exporter.
- New preprocessor for sanitised html output.
- New general ``convert_pandoc`` filter to reduce the need to hard-code lists of filters in templates.
- Use pytest, nose dependency to be removed.
- Refactored Exporter code to avoid ambiguity and cyclic dependencies.
- Update to traitlets 4.2 API.
- Fixes for Unicode errors when showing execution errors on Python 2.
- Default math font matches default Palatino body text font.
- General documentation improvements. For example, testing, installation, custom exporters.
- Improved link handling for LaTeX output
- Refactored the automatic id generation.
- New kernel_manager_class configuration option for allowing systems to be set up to resolve kernels in different ways. 
- Kernel errors now will be logged for debugging purposes when executing notebooks. 

4.3
---

`4.3 on GitHub <https://github.com/jupyter/nbconvert/milestones/4.3>`_

- added live widget rendering for html output, nbviewer by extension

4.2
---

`4.2 on GitHub <https://github.com/jupyter/nbconvert/milestones/4.2>`_

- :ref:`Custom Exporters <external_exporters>` can be provided by external packages,
  and registered with nbconvert via setuptools entrypoints.
- allow nbconvert reading from stdin with ``--stdin`` option (write into
  ``notebook`` basename)
- Various ANSI-escape fixes and improvements
- Various LaTeX/PDF export fixes
- Various fixes and improvements for executing notebooks with ``--execute``.

4.1
---

`4.1 on GitHub <https://github.com/jupyter/nbconvert/milestones/4.1>`_

- setuptools fixes for entrypoints on Windows
- various fixes for exporters, including slides, latex, and PDF
- fixes for exceptions met during execution
- include markdown outputs in markdown/html exports

4.0
---

`4.0 on GitHub <https://github.com/jupyter/nbconvert/milestones/4.0>`_
