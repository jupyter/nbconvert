# -*- coding: utf-8 -*-
"""Tools for coloring text in ANSI terminals.
"""

# subset of IPython.utils.ansicolors, which is:
#*****************************************************************************
#       Copyright (C) 2002-2006 Fernando Perez. <fperez@colorado.edu>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#*****************************************************************************

__all__ = ['TermColors']


color_templates = (
        # Dark colors
        ("Black"       , "0;30"),
        ("Red"         , "0;31"),
        ("Green"       , "0;32"),
        ("Brown"       , "0;33"),
        ("Blue"        , "0;34"),
        ("Purple"      , "0;35"),
        ("Cyan"        , "0;36"),
        ("LightGray"   , "0;37"),
        # Light colors
        ("DarkGray"    , "1;30"),
        ("LightRed"    , "1;31"),
        ("LightGreen"  , "1;32"),
        ("Yellow"      , "1;33"),
        ("LightBlue"   , "1;34"),
        ("LightPurple" , "1;35"),
        ("LightCyan"   , "1;36"),
        ("White"       , "1;37"),
        # Blinking colors.  Probably should not be used in anything serious.
        ("BlinkBlack"  , "5;30"),
        ("BlinkRed"    , "5;31"),
        ("BlinkGreen"  , "5;32"),
        ("BlinkYellow" , "5;33"),
        ("BlinkBlue"   , "5;34"),
        ("BlinkPurple" , "5;35"),
        ("BlinkCyan"   , "5;36"),
        ("BlinkLightGray", "5;37"),
        )

def make_color_table(in_class):
    """Build a set of color attributes in a class.

    Helper function for building the :class:`TermColors` and
    :class`InputTermColors`.
    """
    for name,value in color_templates:
        setattr(in_class,name,in_class._base % value)

class TermColors:
    """Color escape sequences.

    This class defines the escape sequences for all the standard (ANSI?)
    colors in terminals. Also defines a NoColor escape which is just the null
    string, suitable for defining 'dummy' color schemes in terminals which get
    confused by color escapes.

    This class should be used as a mixin for building color schemes."""

    NoColor = ''  # for color schemes in color-less terminals.
    Normal = '\033[0m'   # Reset normal coloring
    _base  = '\033[%sm'  # Template for all other colors

# Build the actual color table as a set of class attributes:
make_color_table(TermColors)
