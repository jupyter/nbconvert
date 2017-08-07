
from traitlets import Set, Unicode
from .base import Sieve 


class TagRemoveInputSieve(Sieve):
    
    remove_input_tags = Set(Unicode, default_value=[],
            help=("Tags indicating cells for which input is to be removed,"
                  "matches tags in `cell.metadata.tags`.")).tag(config=True)

    def sieve(self, nb, resources):
        """
        Sieve to apply to each notebook. See base.py for details.
        """
        # Skip sieve if the list of patterns is empty
        if not self.remove_input_tags:
            return nb, resources

        # Filter out cells that meet the conditions
        nb.cells = [self.sieve_cell(cell, resources, index)[0]
                    for index, cell in enumerate(nb.cells)]

        return nb, resources


    def sieve_cell(self, cell, resources, cell_index):
        """
        Apply sieve to individual cell.
        """
        
        if (self.remove_input_tags.intersection(
                cell.get('metadata', {}).get('tags', []))):
            cell.source = None

        return cell, resources
