"""
Module with tests for ansi filters
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from ...tests.base import TestsBase
from ..ansi import strip_ansi, ansi2html, ansi2latex


class TestAnsi(TestsBase):
    """Contains test functions for ansi.py"""

    def test_strip_ansi(self):
        """strip_ansi test"""
        correct_outputs = {
            '\x1b[32m\x1b[1m\x1b[0;44m\x1b[38;2;255;0;255m\x1b[;m\x1b[m': '',
            'hello\x1b[000;34m': 'hello',
            'he\x1b[1;33m\x1b[;36mllo': 'hello',
            '\x1b[;34mhello': 'hello',
            '\x1b[31mh\x1b[31me\x1b[31ml\x1b[31ml\x1b[31mo\x1b[31m': 'hello',
            'hel\x1b[;00;;032;;;32mlo': 'hello',
            'hello': 'hello',
        }

        for inval, outval in correct_outputs.items():
            self.assertEqual(outval, strip_ansi(inval))

    def test_ansi2html(self):
        """ansi2html test"""
        correct_outputs = {
            '\x1b[31m': '',
            'hello\x1b[34m': 'hello',
            'he\x1b[32m\x1b[36mllo': 'he<span class="ansicyan">llo</span>',
            '\x1b[1;33mhello': '<span class="ansiyellow ansibold">hello</span>',
            '\x1b[37mh\x1b[0;037me\x1b[;0037ml\x1b[00;37ml\x1b[;;37mo': '<span class="ansigray">h</span><span class="ansigray">e</span><span class="ansigray">l</span><span class="ansigray">l</span><span class="ansigray">o</span>',
            'hel\x1b[0;32mlo': 'hel<span class="ansigreen">lo</span>',
            'hello': 'hello',
            '\x1b[1mhello\x1b[33mworld\x1b[0m': '<span class="ansibold">hello</span><span class="ansiyellow ansibold">world</span>',
        }

        for inval, outval in correct_outputs.items():
            self.fuzzy_compare(outval, ansi2html(inval))

    def test_ansi2latex(self):
        """ansi2latex test"""
        correct_outputs = {
            '\x1b[31m': '',
            'hello\x1b[34m': 'hello',
            'he\x1b[32m\x1b[36mllo': r'he\textcolor{cyan}{llo}',
            '\x1b[1;33mhello': r'\textcolor{brown}{\textbf{hello}}',
            '\x1b[37mh\x1b[0;037me\x1b[;0037ml\x1b[00;37ml\x1b[;;37mo': r'\textcolor{lightgray}{h}\textcolor{lightgray}{e}\textcolor{lightgray}{l}\textcolor{lightgray}{l}\textcolor{lightgray}{o}',
            'hel\x1b[0;32mlo': r'hel\textcolor{green}{lo}',
            'hello': 'hello',
            'hello\x1b[34mthere\x1b[mworld': r'hello\textcolor{blue}{there}world',
            'hello\x1b[mthere': 'hellothere',
            'hello\x1b[01;34mthere': r'hello\textcolor{blue}{\textbf{there}}',
            'hello\x1b[001;34mthere': r'hello\textcolor{blue}{\textbf{there}}',
            '\x1b[1mhello\x1b[33mworld\x1b[0m': r'\textbf{hello}\textcolor{brown}{\textbf{world}}',
        }

        for inval, outval in correct_outputs.items():
            self.fuzzy_compare(outval, ansi2latex(inval), case_sensitive=True)
