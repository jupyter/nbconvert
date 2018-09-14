.. _changelog:

====================
Changes in nbconvert
====================

5.4
---
`5.4 on Github <https://github.com/jupyter/nbconvert/milestones/5.4>`__

Significant Changes
~~~~~~~~~~~~~~~~~~~

Deprecations
++++++++++++

Python 3.3 support was dropped. The version of python is no longer common and new versions have many fixes and interface improvements that warrant the change in support.

See :ghpull:`843` for implementation details.

Changes in how we handle metadata
+++++++++++++++++++++++++++++++++

There were a few new metadata fields which are now respected in nbconvert.

``nb.metadata.authors`` metadata attribute will be respected in latex exports. Multiple authors will be added with ``,`` separation against their names.

``nb.metadata.title`` will be respected ahead of ``nb.metadata.name`` for title assignment. This better matches with the notebook format.

``nb.metadata.filename`` will override the default ``output_filename_template`` when extracting notebook resources in the ``ExtractOutputPreprocessor``. The attribute is helpful for when you want to consistently fix to a particular output filename, especially when you need to set image filenames for your exports.

The ``raises-exception`` cell tag (``nb.cells[].metadata.tags[raises-exception]``) allows for cell exceptions to not halt execution. The tag is respected in the same way by `nbval <https://github.com/computationalmodelling/nbval>`_ and other notebook interfaces. ``nb.metadata.allow_errors`` will apply this rule for all cells. This feature is toggleable with the ``force_raise_errors`` configuration option.
Errors from executing the notebook can be allowed with a ``raises-exception`` tag on a single cell, or the ``allow_errors`` configurable option for all cells. An allowed error will be recorded in notebook output, and execution will continue.
If an error occurs when it is not explicitly allowed, a ``CellExecutionError`` will be raised.
If ``force_raise_errors`` is True, ``CellExecutionError`` will be raised for any error that occurs while executing the notebook. This overrides both the ``allow_errors`` option and the ``raises-exception`` cell tags.

See :ghpull:`867`, :ghpull:`703`, :ghpull:`685`, :ghpull:`672`, and :ghpull:`684` for implementation changes.

Configurable kernel managers when executing notebooks
+++++++++++++++++++++++++++++++++++++++++++++++++++++

The kernel manager can now be optionally passed into the ``ExecutePreprocessor.preprocess`` and the ``executenb`` functions as the keyword argument ``km``. This means that the kernel can be configured as desired before beginning preprocessing.

This is useful for executing in a context where the kernel has external dependencies that need to be set to non-default values. An example of this might be a Spark kernel where you wish to configure the Spark cluster location ahead of time without building a new kernel.

Overall the ExecutePreprocessor has been reworked to make it easier to use. Future releases will continue this trend to make this section of the code more inheritable and reusable by others. We encourage you read the source code for this version if you're interested in the detailed improvements.

See :ghpull:`852` for implementation changes.

Surfacing exporters in front-ends
+++++++++++++++++++++++++++++++++

Exporters are now exposed for front-ends to consume, including classic notebook. As an example, this means that latex exporter will be made available for latex 'text/latex' media type from the Download As interface.

See :ghpull:`759` and :ghpull:`864` for implementation changes.

Raw Templates
+++++++++++++

Template exporters can now be assigned raw templates as string attributes by setting the ``raw_template`` variable.

.. code-block:: python

  class AttrExporter(TemplateExporter):
      # If the class has a special template and you want it defined within the class
      raw_template = """{%- extends 'rst.tpl' -%}
  {%- block in_prompt -%}
  raw template
  {%- endblock in_prompt -%}
      """
  exporter_attr = AttrExporter()
  output_attr, _ = exporter_attr.from_notebook_node(nb)
  assert "raw template" in output_attr

See :ghpull:`675` for implementation changes.

New command line flags
++++++++++++++++++++++

The ``--no-input`` will hide input cells on export. This is great for notebooks which generate "reports" where you want the code that was executed to not appear by default in the extracts.

An alias for ``notebook`` was added to exporter commands. Now ``--to ipynb`` will behave as ``--to notebook`` does.

See :ghpull:`825` and :ghpull:`873` for implementation changes.

Comprehensive notes
~~~~~~~~~~~~~~~~~~~

New Features
++++++++++++
- No input flag (``--no-input``) :ghpull:`825`
- Add alias ``--to ipynb`` for notebook exporter :ghpull:`873`
- Add ``export_from_notebook`` :ghpull:`864`
- If set, use ``nb.metadata.authors`` for LaTeX author line :ghpull:`867`
- Populate language_info metadata when executing :ghpull:`860`
- Support for ``\mathscr`` :ghpull:`830`
- Allow the execute preprocessor to make use of an existing kernel :ghpull:`852`
- Refactor ExecutePreprocessor :ghpull:`816`
- Update widgets CDN for ipywidgets 7 w/fallback :ghpull:`792`
- Add support for adding custom exporters to the "Download as" menu. :ghpull:`759`
- Enable ANSI underline and inverse :ghpull:`696`
- Update notebook css to 5.4.0 :ghpull:`748`
- Change default for slides to direct to the reveal cdn rather than locally :ghpull:`732`
- Use "title" instead of "name" for metadata to match the notebook format :ghpull:`703`
- Img filename metadata :ghpull:`685`
- Added MathJax compatibility definitions :ghpull:`687`
- Per cell exception :ghpull:`684`
- Simple API for in-memory templates :ghpull:`674` :ghpull:`675`
- Set BIBINPUTS and BSTINPUTS environment variables when making PDF :ghpull:`676`
- If ``nb.metadata.title`` is set, default to that for notebook :ghpull:`672`

Deprecations
++++++++++++
- Drop support for python 3.3 :ghpull:`843`

Fixing Problems
+++++++++++++++
- Fix api break :ghpull:`872`
- Don't remove empty cells by default :ghpull:`784`
- Handle attached images in html converter :ghpull:`780`
- No need to check for the channels already running :ghpull:`862`
- Update ``font-awesome`` version for slides :ghpull:`793`
- Properly treat JSON data :ghpull:`847`
- Skip executing empty code cells :ghpull:`739`
- Ppdate log.warn (deprecated) to log.warning :ghpull:`804`
- Cleanup notebook.tex during PDF generation :ghpull:`768`
- Windows unicode error fixed, nosetest added to setup.py :ghpull:`757`
- Better content hiding; template & testing improvements :ghpull:`734`
- Fix Jinja syntax in custom template example. :ghpull:`738`
- Fix for an issue with empty math block :ghpull:`729`
- Add parser for Multiline math for LaTeX blocks :ghpull:`716` :ghpull:`717`
- Use defusedxml to parse potentially untrusted XML :ghpull:`708`
- Fixes for traitlets 4.1 deprecation warnings :ghpull:`695`

Testing, Docs, and Builds
+++++++++++++++++++++++++
- A couple of typos :ghpull:`870`
- Add python_requires metadata. :ghpull:`871`
- Document ``--inplace`` command line flag. :ghpull:`839`
- Fix minor typo in ``usage.rst`` :ghpull:`863`
- Add note about local ``reveal_url_prefix`` :ghpull:`844`
- Move ``onlyif_cmds_exist`` decorator to test-specific utils :ghpull:`854`
- Include LICENSE file in wheels :ghpull:`827`
- Added Ubuntu Linux Instructions :ghpull:`724`
- Check for too recent of pandoc version :ghpull:`814` :ghpull:`872`
- Removing more nose remnants via dependencies. :ghpull:`758`
- Remove offline statement and add some clarifications in slides docs :ghpull:`743`
- Linkify PR number :ghpull:`710`
- Added shebang for python :ghpull:`694`
- Upgrade mistune dependency :ghpull:`705`
- add feature to improve docs by having links to prs :ghpull:`662`
- Update notebook CSS from version 4.3.0 to 5.1.0 :ghpull:`682`
- Explicitly exclude or include all files in Manifest. :ghpull:`670`

5.3.1
-----
`5.3.1 on Github <https://github.com/jupyter/nbconvert/milestones/5.3.1>`__

- MANIFEST.in updated to include ``LICENSE`` and ``scripts/`` when creating sdist. :ghpull:`666`

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
