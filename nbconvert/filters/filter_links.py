#!/usr/bin/env python3
"""A pandoc filter used in converting notebooks to Latex.
Converts links between notebooks to Latex cross-references.
"""
import re

from pandocfilters import applyJSONFilters, RawInline

def wrapped_convert_link(source):
    return applyJSONFilters([convert_link], source)

def convert_link(key, val, fmt, meta):
    """
    """
    
    if key == 'Link':
        target = val[2][0]
        # Links to other notebooks
        m = re.match(r'(\d+\-.+)\.ipynb$', target)
        if m:
            return RawInline('tex', 'Section \\ref{sec:%s}' % m.group(1))
            
        # Links to sections of this or other notebooks
        m = re.match(r'(\d+\-.+\.ipynb)?#(.+)$', target)
        if m:
            # pandoc automatically makes labels for headings.
            label = m.group(2).lower()
            label = re.sub(r'[^\w-]+', '', label) # Strip HTML entities
            return RawInline('tex', 'Section \\ref{%s}' % label)

    # Other elements will be returned unchanged.

