.. _changelog:

====================
Changes in nbconvert
====================

6.4.4
-----
* HTMLExporter: Respect the embed_images flag for HTML blocks :ghpull:`1721`

6.4.3
-----
* Remove ipython genutils :ghpull:`1727`
* Add section to customizing showing how to use template inheritance :ghpull:`1719`

6.4.2
-----
* Adding theme support for WebPDF exporter :ghpull:`1718`
* Add option to embed_images in Markdown cells :ghpull:`1717`
* HTMLExporter: Add theme alias and docs :ghpull:`1716`
* Add basic support for federated labextensions themes :ghpull:`1703`
* Always hide the collapser element :ghpull:`1712) 
* Raise pyppeteer requirement to >=1,<1.1 :ghpull:`1711`

6.4.1
-----
* Handle needs_background cell metadata :ghpull:`1704`
* Fix styling regression :ghpull:`1708`
* Fix DOM structure of markdown cells in lab template :ghpull:`1709`
* CodeMirror style bleed fix :ghpull:`1710`

6.4.0
-----

The full list of changes can be seen on the `6.4.0 milestone <https://github.com/jupyter/nbconvert/milestone/23?closed=1>`__

* Allow passing extra args to code highlighter :ghpull:`1683`
* Prevent page breaks in outputs when printing :ghpull:`1679`
* Add collapsers to template :ghpull:`1689`
* Optionally speed up validation :ghpull:`1672`

6.3.0
-----

The full list of changes can be seen on the `6.3.0 milestone <https://github.com/jupyter/nbconvert/milestone/22?closed=1>`__

* Update state filter :ghpull:`1664`
* Add slide numbering :ghpull:`1654`
* Fix HTML templates mentioned in help docs :ghpull:`1653`

6.2.0
-----

The full list of changes can be seen on the `6.2.0 milestone <https://github.com/jupyter/nbconvert/milestone/21?closed=1>`__

* Add the ability to fully customize ``widget_renderer_url`` :ghpull:`1614`
* Enable users to customize MathJax URLs :ghpull:`1609`
* Add CLI configuration for disable-chromium-sandbox :ghpull:`1625`
* Enables webpdf to be rendered with templates :ghpull:`1601`
* Adds dejavu :ghpull:`1599`

6.1.0
-----

This release is mostly a long list of bug fixes and capability
additions. Thanks to the many contributors for helping Improve
nbconvert!

The following 31 authors contributed 81 commits.

* Adolph
* Alessandro Finamore
* Angus Hollands
* Atsuo Ishimoto
* Bo
* David Brochart
* Frédéric Collonval
* Jeremy Howard
* Jim Zwartveld
* José Ignacio Romero
* Joyce Er
* joyceerhl
* Kyle Cutler
* Leah E. Cole
* Leah Wasser
* Nihiue
* Matthew Seal
* Michael Adolph
* Mohammad Mostafa Farzan
* Okky Mabruri
* Pill-GZ
* ptcane
* Raniere Silva
* Ryan Moe
* Stefan Lang
* Sylvain Corlay
* Tobin Jones
* txoof
* Yuvi Panda

Significant Changes
~~~~~~~~~~~~~~~~~~~

* Dropped Python 3.6 and added Python 3.9 :ghpull:`1542`: and :ghpull:`1556`:
* Convert execute preprocessor wrapper to resemble papermill :ghpull:`1448`:

Comprehensive notes
~~~~~~~~~~~~~~~~~~~

* Feature: support static widgets in Reveal.js slides :ghpull:`1553`:
* Feature: add speaker notes to Reveal.js template :ghpull:`1543`:
* Add correct output mimetype to WebPDF exporter :ghpull:`1534`:
* Set mimetype for webpdf correctly :ghpull:`1514`:
* Fix docstring issue and a broken  link :ghpull:`1576`:
* Add CLI example for removing cell tag syntax :ghpull:`1504`:
* Include output of stdin stream in lab template :ghpull:`1454`:
* Don't use a shell to call inkscape :ghpull:`1512`:
* JupyterLab export as HTML with widgets fails to load widgets :ghpull:`1474`:
* Move note inside Reveal.js HTML slideshow :ghpull:`1510`:
* fix issue 1507: broken command line option --CSSHTMLHeaderPreprocessor.style= :ghpull:`1548`:
* Fix order of template paths :ghpull:`1496`:
* Changed documentation of external_exporters :ghpull:`1582`:
* Fix template precedence when using a custom template (#1558) :ghpull:`1577`:
* add  pip to docs  envt :ghpull:`1571`:
* Fix CI  By Adding PIP to  conda envt for docs build :ghpull:`1570`:
* Explicitly install pip in docs environment.yml :ghpull:`1569`:
* small update to docs hide cell :ghpull:`1567`:
* Allow child templates to override mathjax :ghpull:`1551`:
* Allow get_export_names to skip configuration check :ghpull:`1471`:
* Update docs: Tex Live package on Ubuntu :ghpull:`1555`:
* Test jupyter_client :ghpull:`1545`:
* Update jupyterlab css :ghpull:`1539`:
* Webpdf: Use a temporary file instead of an URL  :ghpull:`1489`:
* Applied patch for marking network changes :ghpull:`1527`:
* Change webpdf display name :ghpull:`1515`:
* Allow disabling pyppeteer sandbox :ghpull:`1516`:
* Make pagination configurable in webpdf :ghpull:`1513`:
* Fix Reveal.js version in documentation :ghpull:`1509`:
* Fix dangling reference to get_template_paths() :ghpull:`1463`:
* Solved svg2pdf conversion error if Inkscape is installed into the default path on a windows machine :ghpull:`1469`:
* fix typo :ghpull:`1499`:
* Update version dependency of traitlets :ghpull:`1498`:
* Update execute.py :ghpull:`1457`:
* Fix code output indentation when running nbconvert --no-input :ghpull:`1444`:
* fix issue (i'd call it a BUG) #1167 :ghpull:`1450`:
* #1428 add docstring :ghpull:`1433`:
* Update nbconvert_library.ipynb :ghpull:`1438`:
* Supports isolated iframe when converting to HTML :ghpull:`1593`

6.0.7
-----

Primarly a release addressing template extensions issues reported since 6.0 launched.

Comprehensive notes
~~~~~~~~~~~~~~~~~~~

- Comment typo fix :ghpull:`1425`:
- Documented updated to default conversion changes from 6.0 :ghpull:`1426`:
- Allow custom template files outside of the template system to set their base template name :ghpull:`1429`:
- Restored basic template from 5.x :ghpull:`1431`:
- Added proper support for backwards compatibility templates :ghpull:`1431`:

6.0.6
-----

A range of bug fixes for webpdf exports

Comprehensive notes
~~~~~~~~~~~~~~~~~~~

- Removed CSS preprocessor from default proprocessor list (fixes classic rendering) :ghpull:`1411`:
- Fixed error when pickling TemplateExporter :ghpull:`1399`:
- Support for fractional height html / webpdf exports :ghpull:`1413`:
- Added short wait time for fonts and rendering in webpdf :ghpull:`1414`:
- Updated template documentation
- Minor fixes to the webpdf exporter :ghpull:`1419`:
- Fixup use with a running event loop within webpdf :ghpull:`1420`:
- Prevent overflow in input areas in lab template :ghpull:`1422`:

6.0.5
-----

- Revert networkidle2 change which caused custom cdn-fetched widgets in webpdf

6.0.4
-----

Comprehensive notes
~~~~~~~~~~~~~~~~~~~

Fixing Problems
+++++++++++++++
- The webpdf exporters does not add pagebreaks anymore before reaching the maximum height allowed by Adobe :ghpull:`1402`:
- Fixes some timeout issues with the webpdf exporter :ghpull:`1400`:

6.0.3
-----

Execute preprocessor no longer add illegal execution counts to markdown cells :ghpull:`1396`:

6.0.2
-----

A patch for a few minor issues raised out of the 6.0 release.

Comprehensive notes
~~~~~~~~~~~~~~~~~~~

Fixing Problems
+++++++++++++++
- Added windows work-around fix in CLI for async applications :ghpull:`1383`:
- Fixed pathed template files to behave correctly for local relative paths without a dot :ghpull:`1381`:
- ExecuteProcessor now properly has a ``preprocess_cell`` function to overwrite :ghpull:`1380`:

Testing, Docs, and Builds
+++++++++++++++++++++++++
- Updated README and docs with guidance on how to get help with nbconvert :ghpull:`1377`:
- Fixed documentation that was referencing ``template_path`` instead of ``template_paths`` :ghpull:`1374`:

6.0.1
-----

A quick patch to fix an issue with get_exporter :ghpull:`1367`:

6.0
---

The following authors and reviewers contributed the changes for this release -- Thanks you all!

* Ayaz Salikhov
* bnables
* Bo
* David Brochart
* David Cortés
* Eric Wieser
* Florian Rathgeber
* Ian Allison
* James Wilshaw
* Jeremy Tuloup
* Joel Ostblom
* Jon Bannister
* Jonas Drotleff
* Josh Devlin
* Karthikeyan Singaravelan
* Kerwin.Sun
* letmerecall
* Luciano Resende
* Lumír 'Frenzy' Balhar
* Maarten A. Breddels
* Maarten Breddels
* Marcel Stimberg
* Matthew Brett
* Matthew Seal
* Matthias Bussonnier
* Matthias Geier
* Miro Hrončok
* Phil Austin
* Praveen Batra
* Ruben Di Battista
* Ruby Werman
* Sang-Yun Oh
* Sergey Kizunov
* Sundar
* Sylvain Corlay
* telamonian
* Thomas Kluyver
* Thomas Ytterdal
* Tyler Makaro
* Yu-Cheng (Henry) Huang

Significant Changes
~~~~~~~~~~~~~~~~~~~

Nbconvert 6.0 is a major release of nbconvert which includes many significant changes.

- Python 2 support was dropped. Currently Python 3.6-3.8 is supported and tested by nbconvert. However, nbconvert 6.0 provides limited support for Python 3.6. nbconvert 6.1 will drop support for Python 3.6. Limited support means we will test and run CI on Python 3.6.12 or higher. Issues that are found only affecting Python 3.6 are not guaranteed to be fixed. We recommend all users of nbconvert use Python 3.7 and higher.

- Unlike previous versions, nbconvert 6.0 relies on the `nbclient <https://github.com/jupyter/nbclient/>`__ package for the execute preprocessor, which allows for asynchronous kernel requests.

- ``template_path`` has become ``template_paths``. If referring to a 5.x style ``.tpl`` template use the full path with the ``template_file`` argument to the file. On the command line the pattern is ``--template-file=<path/to/file.tpl>``.

- Nbconvert 6.0 includes a new "webpdf" exporter, which renders notebooks in pdf format through a headless web browser, so that complex outputs such as HTML tables, or even widgets are rendered in the same way as with the HTML exporter and a web browser.

- The default template applied when exporting to HTML now produces the same DOM structure as JupyterLab, and is styled using JupyterLab's CSS. The pygments theme in use mimics JupyterLab's codemirror mode with the same CSS variables, so that custom JupyterLab themes could be applied. The classic notebook styling can still be enabled with

.. code-block:: bash

   jupyter nbconvert --to html --template classic

- Nbconvert 6.0 includes a new system for creating custom templates, which can now be installed as packages. A custom "foobar" template is installed in Jupyter's data directory under ``nbconvert/templates`` and has the form of a directory containing all resources. Templates specify their base template as well as other configuration parameters in a ``conf.json`` at the root of the template directory.

- The "slideshow" template now makes use of RevealJS version 4. It can now be used with the HTML exporter with

.. code-block:: bash

   jupyter nbconvert --to html --template reveal

The ``--to slides`` exporter is still supported for convenience.

- Inkscape 1.0 is now supported, which had some breaking changes that prevented 5.x versions of nbconvert from converting documents on some systems that updated.

Remaining changes
~~~~~~~~~~~~~~~~~

We merged 105 pull requests! Rather than enumerate all of them we'll link to the github page which contains the many smaller impact improvements.

The full list can be seen `on GitHub <https://github.com/jupyter/nbconvert/issues?q=milestone%3A6.0+>`__

5.6.1
-----

The following authors and reviewers contributed the changes for this release -- Thanks you all!

* Charles Frye
* Chris Holdgraf
* Felipe Rodrigues
* Gregor Sturm
* Jim
* Kerwin Sun
* Ryan Beesley
* Matthew Seal
* Matthias Geier
* thuy-van
* Tyler Makaro

Significant Changes
~~~~~~~~~~~~~~~~~~~

RegExRemove applies to all cells
++++++++++++++++++++++++++++++++

RegExRemove preprocessor now removes cells regardless of cell outputs. Before this only cells that had outputs were filtered.

Comprehensive notes
~~~~~~~~~~~~~~~~~~~

New Features
++++++++++++
- Add support for alt tags for jpeg and png images :ghpull:`1112`:
- Allow HTML header anchor text to be HTML :ghpull:`1101`:
- Change RegExRemove to remove code cells with output :ghpull:`1095`:
- Added cell tag data attributes to HTML exporter :ghpull:`1090`: and :ghpull:`1089`:

Fixing Problems
+++++++++++++++
- Update svg2pdf.py to search the PATH for inkscape :ghpull:`1115`:
- Fix latex dependencies installation command for Ubuntu systems :ghpull:`1109`:

Testing, Docs, and Builds
+++++++++++++++++++++++++
- Added Circle CI builds for documentation :ghpull:`1114`: :ghpull:`1120`:, and :ghpull:`1116`:
- Fix typo in argument name in docstring (TagRemovePreprocessor) :ghpull:`1103`:
- Changelog typo fix :ghpull:`1100`:
- Updated API page for TagRemovePreprocessor and TemplateExporter :ghpull:`1088`:
- Added remove_input_tag traitlet to the docstring :ghpull:`1088`:

5.6
---

The following 24 authors and reviewers contributed 224 commits -- Thank you all!

* 00Kai0
* Aidan Feldman
* Alex Rudy
* Alexander Kapshuna
* Alexander Rudy
* amniskin
* Carol Willing
* Dustin H
* Hsiaoming Yang
* imtsuki
* Jessica B. Hamrick
* KrokodileDandy
* Kunal Marwaha
* Matthew Seal
* Matthias Geier
* Miro Hrončok
* M Pacer
* Nils Japke
* njapke
* Sebastian Führ
* Sylvain Corlay
* Tyler Makaro
* Valery M
* Wayne Witzel

The full list of changes they made can be seen `on GitHub <https://github.com/jupyter/nbconvert/issues?q=milestone%3A5.6+>`__

Significant Changes
~~~~~~~~~~~~~~~~~~~

Jupter Client Pin
+++++++++++++++++
The ``jupyter_client`` dependency is now pinned to ``>5.3.1``. This is done to support the `Parallel NBConvert`_ below, and future versions may require interface changes from that version.

Parallel NBConvert
++++++++++++++++++
NBConvert ``--execute`` can now be run in parallel via threads, multiprocessing, or async patterns! This means you can now parallelize nbconvert via a bash loop, or a python concurrency pattern and it should be able to execute those notebooks in parallel.

Kernels have varying support for safe concurrent execution. The ipython kernel (ipykernel version 1.5.2 and higher) should be safe to run concurrently using Python 3. However, the Python 2 ipykernel does not always provide safe concurrent execution and sometimes fails with a socket bind exception. Unlike ipykernel which is maintained by the project, other community-maintained kernels may have varying support for concurrent execution, and these kernels were not tested heavily.

Issues for nbconvert can be viewed here: :ghpull:`1018`:, and :ghpull:`1017`:

.. note: We'll keep an eye for issues related to this new capability and try to quickly patch any discovered issues post release. The improvement required touching three projects with separate releases, so if you do find an issue try upgrading dependencies and listing your dependencies for your environment when reporting.

Execute Loop Rewrite
++++++++++++++++++++
This release completely rewrote the execution loop responsible for monitoring kernel messages until cell execution is completed. This removes an error where kernel messages could be dropped if too many were posted too quickly. Furthermore, the change means that messages are not buffered. Now, messages can be logged immediately rather than waiting for the cell to terminate.

See :ghpull:`994`: for exact code changes if you're curious.

Comprehensive notes
~~~~~~~~~~~~~~~~~~~

New Features
++++++++++++
- Make a default global location for custom user templates :ghpull:`1028`:
- Parallel execution improvements :ghpull:`1018`:, and :ghpull:`1017`:
- Added ``store_history`` option to ``preprocess_cell`` and ``run_cell`` :ghpull:`1055`:
- Simplify the function signature for preprocess() :ghpull:`1042`:
- Set flag to not always stop kernel execution on errors :ghpull:`1040`:
- ``setup_preprocessor`` passes kwargs to ``start_new_kernel`` :ghpull:`1021`:

Fixing Problems
+++++++++++++++
- Very fast stream outputs no longer drop some messages :ghpull:`994`:
- LaTeX errors now properly raise exceptions :ghpull:`1053`:
- Improve template whitespacing :ghpull:`1076`:
- Fixes for character in LaTeX exports and filters :ghpull:`1068`:, :ghpull:`1039`:, :ghpull:`1024`:, and :ghpull:`1077`:
- Mistune pinned in preparation for 2.0 release :ghpull:`1074`:
- Require mock only on Python 2 :ghpull:`1060`: and :ghpull:`1011`:
- Fix selection of mimetype when converting to HTML :ghpull:`1036`:
- Correct a few typos :ghpull:`1029`:
- Update ``export_from_notebook`` names :ghpull:`1027`:
- Dedenting html in ExtractOutputPreprocessor :ghpull:`1023`:
- Fix backwards incompatibility with markdown2html :ghpull:`1022`:
- Fixed html image tagging :ghpull:`1013`:
- Remove unnecessary css :ghpull:`1010`:

Testing, Docs, and Builds
+++++++++++++++++++++++++
- Pip-install nbconvert on readthedocs.org :ghpull:`1069`:
- Fix various doc build issues :ghpull:`1051`:, :ghpull:`1050`:, :ghpull:`1019`:, and :ghpull:`1048`:
- Add issue templates :ghpull:`1046`:
- Added instructions for bumping the version forward when releasing :ghpull:`1034`:
- Fix Testing on Windows :ghpull:`1030`:
- Refactored ``test_run_notebooks`` :ghpull:`1015`:
- Fixed documentation typos :ghpull:`1009`:

5.5
---

The following 18 authors contributed 144 commits -- Thank you all!

* Benjamin Ragan-Kelley
* Clayton A Davis
* DInne Bosman
* Doug Blank
* Henrique Silva
* Jeff Hale
* Lukasz Mitusinski
* M Pacer
* Maarten Breddels
* Madhumitha N
* Matthew Seal
* Paul Gowder
* Philipp A
* Rick Lupton
* Rüdiger Busche
* Thomas Kluyver
* Tyler Makaro
* WrRan

The full list of changes they made can be seen `on GitHub <https://github.com/jupyter/nbconvert/issues?q=milestone%3A5.5+>`__

Significant Changes
~~~~~~~~~~~~~~~~~~~

Deprecations
++++++++++++

Python 3.4 support was dropped. Many of our upstream libraries stopped supporting 3.4 and it was found that serious bugs were being caught during testing against those libraries updating past 3.4.

See :ghpull:`979` for details.

IPyWidget Support
+++++++++++++++++

Now when a notebook executing contains `Jupyter Widgets <https://github.com/jupyter-widgets/ipywidgets/>`__, the state of all the widgets can be stored in the notebook's metadata. This allows rendering of the live widgets on, for instance nbviewer, or when converting to html.

You can tell nbconvert to not store the state using the ``store_widget_state`` argument::

     jupyter nbconvert --ExecutePreprocessor.store_widget_state=False --to notebook --execute mynotebook.ipynb

This widget rendering is not performed against a browser during execution, so only widget default states or states manipulated via user code will be calculated during execution. ``%%javascript`` cells will execute upon notebook rendering, enabling complex interactions to function as expected when viewed by a UI.

If you can't view widget results after execution, you may need to select
:menuselection:`File --> Trust Notebook` in the menu.

See :ghpull:`779`, :ghpull:`900`, and :ghpull:`983` for details.

Execute Preprocessor Rework
+++++++++++++++++++++++++++

Based on monkey patching required in `papermill <https://github.com/nteract/papermill/blob/0.19.1/papermill/preprocess.py>`__ the ``run_cell`` code path in the ExecutePreprocessor was reworked to allow for accessing individual message parses without reimplementing the entire function. Now there is a ``process_message`` function which take a ZeroMQ message and applies all of its side-effect updates on the cell/notebook objects before returning the output it generated, if it generated any such output.

The change required a much more extensive test suite covering cell execution as test coverage on the various, sometimes wonky, code paths made improvements and reworks impossible to prove undamaging. Now changes to kernel message processing has much better coverage, so future additions or changes with specs over time will be easier to add.

See :ghpull:`905` and :ghpull:`982` for details

Out Of Memory Kernel Failure Catches
++++++++++++++++++++++++++++++++++++

When running out of memory on a machine, if the kernel process was killed by the operating system it would result in a timeout error at best and hang indefinitely at worst. Now regardless of timeout configuration, if the underlying kernel process dies before emitting any messages to the effect an exception will be raised notifying the consumer of the lost kernel within a few seconds.

See :ghpull:`959`, :ghpull:`971`, and :ghpull:`998` for details

Latex / PDF Template Improvements
+++++++++++++++++++++++++++++++++

The latex template was long overdue for improvements. The default template had a rewrite which makes exports for latex and pdf look a lot better. Code cells in particular render much better with line breaks and styling the more closely matches notebook browser rendering. Thanks t-makaro for the efforts here!

See :ghpull:`992` for details

Comprehensive notes
~~~~~~~~~~~~~~~~~~~

New Features
++++++++++++
- IPyWidget Support :ghpull:`779`, :ghpull:`900`, and :ghpull:`983`
- A new ClearMetadata Preprocessor is available :ghpull:`805`:
- Support for pandoc 2 :ghpull:`964`:
- New, and better, latex template :ghpull:`992`:

Fixing Problems
+++++++++++++++
- Refactored execute preprocessor to have a process_message function :ghpull:`905`:
- Fixed OOM kernel failures hanging :ghpull:`959` and :ghpull:`971`:
- Fixed latex export for svg data in python 3 :ghpull:`985`:
- Enabled configuration to be shared to exporters from script exporter :ghpull:`993`:
- Make latex errors less verbose :ghpull:`988`:
- Typo in template syntax :ghpull:`984`:
- Improved attachments +fix supporting non-unique names :ghpull:`980`:
- PDFExporter "output_mimetype" traitlet is not longer 'text/latex' :ghpull:`972`:
- FIX: respect wait for clear_output :ghpull:`969`:
- address deprecation warning in cgi.escape :ghpull:`963`:
- Correct inaccurate description of available LaTeX template :ghpull:`958`:
- Fixed kernel death detection for executions with timeouts :ghpull:`998`:
- Fixed export names for various templates :ghpull:`1000`, :ghpull:`1001`, and :ghpull:`1001`:

Deprecations
++++++++++++
- Dropped support for python 3.4 :ghpull:`979`:
- Removed deprecated ``export_by_name`` :ghpull:`945`:

Testing, Docs, and Builds
+++++++++++++++++++++++++
- Added tests for each branch in execute's run_cell method :ghpull:`982`:
- Mention formats in --to options more clearly :ghpull:`991`:
- Adds ascii output type to command line docs page, mention image folder output :ghpull:`956`:
- Simplify setup.py :ghpull:`949`:
- Use utf-8 encoding in execute_api example :ghpull:`921`:
- Upgrade pytest on Travis :ghpull:`941`:
- Fix LaTeX base template name in docs :ghpull:`940`:
- Updated release instructions based on 5.4 release walk-through :ghpull:`887`:
- Fixed broken link to jinja docs :ghpull:`997`:

5.4.1
-----
`5.4.1 on Github <https://github.com/jupyter/nbconvert/milestones/5.4.1>`__

Thanks to the following 11 authors who contributed 57 commits.

* Benjamin Ragan-Kelley
* Carol Willing
* Clayton A Davis
* Daniel Rodriguez
* M Pacer
* Matthew Seal
* Matthias Geier
* Matthieu Parizy
* Rüdiger Busche
* Thomas Kluyver
* Tyler Makaro

Comprehensive notes
~~~~~~~~~~~~~~~~~~~

New Features
++++++++++++
- Expose pygments styles :ghpull:`889`:
- Tornado 6.0 support -- Convert proxy handler from callback to coroutine :ghpull:`937`:
- Add option to overwrite the highlight_code filter :ghpull:`877`:

Fixing Problems
+++++++++++++++
- Mathjax.tpl fix for rendering Latex in html :ghpull:`932`:
- Backwards compatbility for empty kernel names :ghpull:`927` :ghpull:`924`

Testing, Docs, and Builds
+++++++++++++++++++++++++
- DOC: Add missing language specification to code-block :ghpull:`882`:

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
If an error occurs when it is not explicitly allowed, a 'CellExecutionError' will be raised.
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
- Default conversion method on the CLI was removed (``--to html`` now required)

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
metadata <https://nbformat.readthedocs.io/en/latest/format_description.html#cell-metadata>`__.

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
- new: function for executing notebooks: ``executenb`` :ghpull:`573`
- new: global filtering to remove inputs, outputs, markdown cells (&c.), this works on all templates :ghpull:`554`
- new: script exporter entrypoint :ghpull:`531`
- new: configurable anchor link text (previously ¶) ``HTMLExporter.anchor_link_text`` :ghpull:`522`

- new: configurable values for slides exporter :ghpull:`542` :ghpull:`558`

- improved releases (how-to documentation, version-number generation and checking) :ghpull:`593`
- doc improvements  :ghpull:`593` :ghpull:`580` :ghpull:`565` :ghpull:`554`
- language information from cell magics (for highlighting) is now included in more formats :ghpull:`586`
- mathjax upgrades and cdn fixes :ghpull:`584` :ghpull:`567`
- better CI :ghpull:`571` :ghpull:`540`
- better traceback behaviour when execution errs :ghpull:`521`
- deprecated nose test features removed :ghpull:`519`

- bug fixed: we now respect width and height metadata on jpeg and png mimetype outputs :ghpull:`588`
- bug fixed: now we respect the ``resolve_references`` filter in ``report.tplx`` :ghpull:`577`
- bug fixed: output metadata now is removed by ClearOutputPreprocessor :ghpull:`569`
- bug fixed: display id respected in execute preproessor :ghpull:`563`
- bug fixed: dynamic defaults for optional jupyter_client import :ghpull:`559`
- bug fixed: don't self-close non-void HTML tags :ghpull:`548`
- buf fixed: upgrade jupyter_client dependency to 4.2 :ghpull:`539`
- bug fixed: LaTeX output through md→LaTeX conversion shouldn't be touched :ghpull:`535`
- bug fixed: now we escape ``<`` inside math formulas when converting to html :ghpull:`514`

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
