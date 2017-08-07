"""Base class for sieves"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from ..utils.base import NbConvertBase
from traitlets import Bool


class Sieve(NbConvertBase):
    """ A configurable sieve

    Inherit from this class if you wish to have a configurable sieve.

    Any configurable traitlets this class exposes will be configurable in
    profiles using c.SubClassName.attribute = value

    You can overwrite :meth:`sieve_cell` to apply a transformation
    independently on each cell or :meth:`sieve` if you prefer your own
    logic. See corresponding docstring for further information.

    Disabled by default and can be enabled via the config by
        'c.YourSieveName.enabled = True'
    """

    enabled = Bool(False).tag(config=True)

    def __init__(self, **kw):
        """
        Public constructor

        Parameters
        ----------
        config : Config
            Configuration file structure
        `**kw`
            Additional keyword arguments passed to parent
        """

        super(Sieve, self).__init__(**kw)

    def __call__(self, nb, resources):
        if self.enabled:
            self.log.debug("Applying sieve: %s",
                           self.__class__.__name__)
            return self.sieve(nb, resources)
        else:
            return nb, resources

    def sieve(self, nb, resources):
        """
        Sieve to apply on each notebook.

        Must return modified nb, resources.

        If you wish to apply your sieve to each cell, you might want
        to override sieve_cell method instead.

        Parameters
        ----------
        nb : NotebookNode
            Notebook being converted
        resources : dictionary
            Additional resources used in the conversion process.  Allows
            sieves to pass variables into the Jinja engine.
        """
        for ind, cell in enumerate(nb.cells):
            nb.cells[ind], resources = self.sieve_cell(cell, resources, ind)
        return nb, resources

    def sieve_cell(self, cell, resources, index):
        """
        Override if you want to sieve each cell.
        Must return modified cell and resource dictionary.

        Parameters
        ----------
        cell : NotebookNode cell
            Notebook cell being sieved
        resources : dictionary
            Additional resources used in the conversion process.  Allows
            sieves to pass variables into the Jinja engine.
        index : int
            Index of the cell being sieved
        """

        raise NotImplementedError('should be implemented by subclass')
        return cell, resources
