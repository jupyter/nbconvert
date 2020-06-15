"""Base class for processors"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from ..utils.base import NbConvertBase
from traitlets import Bool


class Processor(NbConvertBase):
    """ A configurable Processor

    Inherit from this class if you wish to have configurability for your
    Processor.

    Any configurable traitlets this class exposed will be configurable in
    profiles using c.SubClassName.attribute = value

    you can overwrite :meth:`processor_cell` to apply a transformation
    independently on each cell or :meth:`process` if you prefer your own
    logic. See corresponding docstring for information.

    Disabled by default and can be enabled via the config by
        'c.YourProcessorName.enabled = True'
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
        
        super().__init__(**kw)

    def __call__(self, nb, resources):
        if self.enabled:
            self.log.debug("Applying Processor: %s",
                           self.__class__.__name__)
            return self.process(nb, resources)
        else:
            return nb, resources

    def process(self, nb, resources):
        """
        Processing to apply on each notebook.
        
        Must return modified nb, resources.
        
        If you wish to apply your processoring to each cell, you might want
        to override processor_cell method instead.
        
        Parameters
        ----------
        nb : NotebookNode
            Notebook being converted
        resources : dictionary
            Additional resources used in the conversion process.  Allows
            processors to pass variables into the Jinja engine.
        """
        for index, cell in enumerate(nb.cells):
            nb.cells[index], resources = self.process_cell(cell, resources, index)
        return nb, resources

    def processor_cell(self, cell, resources, index):
        from warnings import warn
        warn(f"Calling 'processor_cell' on Processor is deprecated since version 6.0.0 and has been replaced by 'process_cell'",
            DeprecationWarning)
        self.process_cell(cell, resources, index)

    def processor(self, nb, resources):
        from warnings import warn
        warn(f"Calling 'processor' on Processor is deprecated since version 6.0.0 and has been replaced by 'process'",
            DeprecationWarning)
        self.process(nb, resources)
