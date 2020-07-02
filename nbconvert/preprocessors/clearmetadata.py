"""Module containing a preprocessor that removes metadata from code cells"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from traitlets import Bool, Set
from .base import Preprocessor

class ClearMetadataPreprocessor(Preprocessor):
    """
    Removes all the metadata from all code cells in a notebook.
    """

    clear_notebook_metadata = Bool(True,
        help=("Flag to choose if notebook metadata is to be cleared "
              "in addition to cell metadata.")).tag(config=True)
    preserve_metadata_keys = Set(
        help=("Indicates the keys to preserve when deleting metadata "
               "across both cells and notebook metadata fields.")).tag(config=True)

    def preprocess_cell(self, cell, resources, cell_index):
        """
        All the code cells are returned with an empty metadata field.
        """
        if cell.cell_type == 'code':
            # Remove metadata
            if 'metadata' in cell:
                cell.metadata = { k: v for k,v in cell.metadata.items() if k in self.preserve_metadata_keys }
        return cell, resources

    def preprocess(self, nb, resources):
        """
        Preprocessing to apply on each notebook.
        
        Must return modified nb, resources.
        
        Parameters
        ----------
        nb : NotebookNode
            Notebook being converted
        resources : dictionary
            Additional resources used in the conversion process.  Allows
            preprocessors to pass variables into the Jinja engine.
        """
        nb, resources = super().preprocess(nb, resources)
        if self.clear_notebook_metadata:
            if 'metadata' in nb:
                nb.metadata = { k: v for k,v in nb.metadata.items() if k in self.preserve_metadata_keys }
        return nb, resources
