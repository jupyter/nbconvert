#!/usr/bin/env python3
"""A pandoc filter used in converting notebooks to Latex.
Converts links between notebooks to Latex cross-references.
"""
import re

from pandocfilters import RawInline, applyJSONFilters

def resolve_references(source):
    return applyJSONFilters([resolve_one_reference], source)

def resolve_one_reference(key, val, fmt, meta):
    """
    """
    
    if key == 'Link':
        target = val[2][0]
        m = re.match(r'#(.+)$', target)
        if m:
            # pandoc automatically makes labels for headings.
            label = m.group(1).lower()
            label = re.sub(r'[^\w-]+', '', label) # Strip HTML entities
            return RawInline('tex', r'Section \ref{%s}' % label)

    # Other elements will be returned unchanged.

