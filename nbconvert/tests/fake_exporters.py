"""
Module that define a custom exporter just to test the ability to invoke
nbconvert with full qualified name
"""
from nbconvert.exporters.html import HTMLExporter

#-----------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------

class MyExporter(HTMLExporter):
    """
    My custom exporter  
    """
    
    def _file_extension_default(self):
        """
        The new file extension is `.test_ext`
        """
        return '.test_ext'
