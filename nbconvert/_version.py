from nbconvert._version_tools import create_valid_version

version_info = (5, 2, 0)
pre_info = ''
dev_info = '.dev'
__version__ = create_valid_version(version_info, pre_input=pre_info, dev_input=dev_info) 

