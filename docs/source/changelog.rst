Changes in nbconvert
====================

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
