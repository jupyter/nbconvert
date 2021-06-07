.. _nbconvert_release:

Making an ``nbconvert`` release
===============================

This document guides a contributor through creating a release of ``nbconvert``.


Assign all merged PRs to milestones
-----------------------------------

Go to GitHub and assign all PRs that have been merged to milestones.  This will
be helpful when you update the changelog. If you go to this `GitHub page <Github
no milestones_>`_ you will find all the PRs that currently have no milestones.

.. _GitHub no milestones: https://github.com/jupyter/nbconvert/pulls?utf8=%E2%9C%93&q=is%3Amerged%20is%3Apr%20no%3Amilestone%20

Gather all PRs related to milestone
-----------------------------------

`ghpro <ghpro_>`_ can be used to extract the pull requests by call the following from nbconvert directory (will ask for an API token the first time):

    .. code:: bash

        github-stats --milestone=$VERSION --since-tag $LAST_VERSION --links

.. _ghpro: https://github.com/mpacer/ghpro/tree/alternate_styling

Manually categorize tickets
---------------------------

Group the tickets by these general categories (or others if they are relevant). This usually a manual processes to evaluate the changes in each PR.

#. New Features
#. Deprecations
#. Fixing Problems
#. Testing, Docs, and Builds

Collect major changes
---------------------

From the tickets write up any major features / changes that deserve a paragraph to describe how they work.

Update docs/source/changelog.rst
--------------------------------

Copy these changes with the new version to the top of changelog.rst. Prior release changelogs can be used to pick formatting of the message.

Check installed tools
---------------------

Review ``CONTRIBUTING.md``, particularly the testing and release sections.

Clean the repository
--------------------

You can remove all non-tracked files with:

    .. code:: bash

        git clean -xfdi

This would ask you for confirmation before removing all untracked files.

Make sure the ``dist/`` and ``build/`` folders are clean and avoid stale builds from
previous attempts.

Create the release
------------------

#.  Update the :doc:`changelog <changelog>` to account for all the PRs assigned to this milestone.

#.  Update version number in ``notebook/_version.py`` and remove ``.dev`` from dev_info. Note that the version may already be on the dev version of the number you're releasing.

#.  Commit and tag the release with the current version number:

    .. code:: bash

        git commit -am "release $VERSION"
        git tag $VERSION

#.  You are now ready to build the ``sdist`` and ``wheel``:

    .. code:: bash

        python setup.py sdist
        python setup.py bdist_wheel

#.  You can now test the ``wheel`` and the ``sdist`` locally before uploading
    to PyPI. Make sure to use `twine <https://github.com/pypa/twine>`_ to
    upload the archives over SSL.

    .. code:: bash

        twine upload dist/*

#.  The conda-forge bot will automatically add a PR on your behalf to the `nbconvert-feedstock repo <conda-forge-nbconvert_>`_. You may want to review this PR to ensure conda-forge will be updated cleanly.

.. _conda-forge-nbconvert: https://github.com/conda-forge/nbconvert-feedstock

Release the new version
-----------------------

Push directly on main, including --tags separately

    .. code:: bash

        git push upstream
        git push upstream --tags


Return to development state
---------------------------

If all went well, change the ``notebook/_version.py`` back by adding the
    ``.dev`` suffix and moving the version forward to the next patch
    release number.


Email googlegroup with update letter
------------------------------------

Make sure to email jupyter@googlegroups.com with the subject line of "[ANN] NBConvert $VERSION -- ..." and include at least the significant changes, contributors, and individual PR notes (if not many significant changes).
