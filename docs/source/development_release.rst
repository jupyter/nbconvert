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

Check installed tools
---------------------

Review ``CONTRIBUTING.md``, particularly the testing and release sections.

Clean the repository
--------------------

You can remove all non-tracked files with:

.. code:: bash

    git clean -xfdi

This would ask you for confirmation before removing all untracked files. 

Make sure the ``dist/`` folder is clean and avoid stale builds from
previous attempts.

Create the release
------------------

#.  Update the :doc:`changelog <changelog>` to account for all the PRs assigned to this milestone.

#.  Update version number in ``notebook/_version.py``.

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

Release the new version
-----------------------

Push directly on master, including --tags separately
    
    .. code:: bash

        git push upstream 
        git push upstream --tags


Update nbviewer
---------------

On nbviewer-deploy run `invoke trigger_build` and then once it's built on
dockerhub run `invoke doitall`. 

Return to development state
---------------------------

If all went well, change the ``notebook/_version.py`` back adding the
    ``.dev`` suffix.
