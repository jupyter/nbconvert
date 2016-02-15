"""Filters for processing ANSI colors within Jinja templates."""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import re
import jinja2

__all__ = [
    'strip_ansi',
    'ansi2html',
    'ansi2latex'
]

_ANSI_RE = re.compile('\x1b\\[(.*?)([@-~])')

_FG_HTML = (
    'ansiblack',
    'ansired',
    'ansigreen',
    'ansiyellow',
    'ansiblue',
    'ansipurple',
    'ansicyan',
    'ansigray',
)

_BG_HTML = (
    'ansibgblack',
    'ansibgred',
    'ansibggreen',
    'ansibgyellow',
    'ansibgblue',
    'ansibgpurple',
    'ansibgcyan',
    'ansibggray',
)

_FG_LATEX = (
    'black',
    'red',
    'green',
    'brown',
    'blue',
    'purple',
    'cyan',
    'lightgray',
)

_BG_LATEX = (
    'darkgray',
    'lightred',
    'lightgreen',
    'yellow',
    'lightblue',
    'lightpurple',
    'lightcyan',
    'white',
)


def strip_ansi(source):
    """
    Remove ANSI escape codes from text.

    Parameters
    ----------
    source : str
        Source to remove the ANSI from

    """
    return _ANSI_RE.sub('', source)


def ansi2html(text):
    """
    Convert ANSI colors to HTML colors.

    Parameters
    ----------
    text : str
        Text containing ANSI colors to convert to HTML

    """
    text = str(jinja2.utils.escape(text))
    return _ansi2anything(text, _htmlconverter)


def ansi2latex(text):
    """
    Convert ANSI colors to LaTeX colors.

    Parameters
    ----------
    text : str
        Text containing ANSI colors to convert to LaTeX

    """
    return _ansi2anything(text, _latexconverter)


def _htmlconverter(fg, bg, bold):
    """
    Return start and end tags for given foreground/background/bold.

    """
    if (fg, bg, bold) == (None, None, False):
        return '', ''

    classes = []
    styles = []

    if isinstance(fg, int):
        classes.append(_FG_HTML[fg])
    elif fg:
        styles.append('color: rgb({},{},{})'.format(*fg))

    if isinstance(bg, int):
        classes.append(_BG_HTML[bg])
    elif bg:
        styles.append('background-color: rgb({},{},{})'.format(*bg))

    if bold:
        classes.append('ansibold')

    starttag = '<span'
    if classes:
        starttag += ' class="' + ' '.join(classes) + '"'
    if styles:
        starttag += ' style="' + '; '.join(styles) + '"'
    starttag += '>'
    return starttag, '</span>'


def _latexconverter(fg, bg, bold):
    """
    Return start and end markup given foreground/background/bold.

    """
    if (fg, bg, bold) == (None, None, False):
        return '', ''

    starttag, endtag = '', ''

    if isinstance(fg, int):
        starttag += r'\textcolor{' + _FG_LATEX[fg] + '}{'
        endtag = '}' + endtag
    elif fg:
        # See http://tex.stackexchange.com/a/291102/13684
        starttag += r'\def\tcRGB{\textcolor[RGB]}\expandafter'
        starttag += r'\tcRGB\expandafter{\detokenize{%s,%s,%s}}{' % fg
        endtag = '}' + endtag

    if isinstance(bg, int):
        starttag += r'\setlength{\fboxsep}{0pt}\colorbox{'
        starttag += _BG_LATEX[bg] + '}{'
        endtag = r'\strut}' + endtag
    elif bg:
        starttag += r'\setlength{\fboxsep}{0pt}'
        # See http://tex.stackexchange.com/a/291102/13684
        starttag += r'\def\cbRGB{\colorbox[RGB]}\expandafter'
        starttag += r'\cbRGB\expandafter{\detokenize{%s,%s,%s}}{' % bg
        endtag = r'\strut}' + endtag

    if bold:
        starttag += r'\textbf{'
        endtag = '}' + endtag
    return starttag, endtag


def _ansi2anything(text, converter):
    r"""
    Convert ANSI colors to HTML or LaTeX.

    See https://en.wikipedia.org/wiki/ANSI_escape_code

    Accepts codes like '\x1b[32m' (red) and '\x1b[1;32m' (bold, red).
    The codes 1 (bold) and 5 (blinking) are selecting a bold font, code
    0 and an empty code ('\x1b[m') reset colors and bold-ness.
    Unlike in most terminals, "bold" doesn't change the color.
    The codes 21 and 22 deselect "bold", the codes 39 and 49 deselect
    the foreground and background color, respectively.
    The codes 38 and 48 select the "extended" set of foreground and
    background colors, respectively.

    Non-color escape sequences (not ending with 'm') are filtered out.

    Ideally, this should have the same behavior as the function
    fixConsole() in notebook/notebook/static/base/js/utils.js.

    """
    fg, bg = None, None
    bold = False
    numbers = []
    out = []

    while text:
        m = _ANSI_RE.search(text)
        if m:
            if m.group(2) == 'm':
                try:
                    numbers = [int(n) if n else 0
                               for n in m.group(1).split(';')]
                except ValueError:
                    pass  # Invalid color specification
            else:
                pass  # Not a color code
            chunk, text = text[:m.start()], text[m.end():]
        else:
            chunk, text = text, ''

        if chunk:
            starttag, endtag = converter(fg, bg, bold)
            out.append(starttag)
            out.append(chunk)
            out.append(endtag)

        while numbers:
            n = numbers.pop(0)
            if n == 0:
                fg = bg = None
                bold = False
            elif n in (1, 5):
                bold = True
            elif n in (21, 22):
                bold = False
            elif 30 <= n <= 37:
                fg = n - 30
            elif n == 38:
                try:
                    fg = _get_extended_color(numbers)
                except ValueError:
                    numbers.clear()
            elif n == 39:
                fg = None
            elif 40 <= n <= 47:
                bg = n - 40
            elif n == 48:
                try:
                    bg = _get_extended_color(numbers)
                except ValueError:
                    numbers.clear()
            elif n == 49:
                bg = None
            else:
                pass  # Unknown codes are ignored
    return ''.join(out)


def _get_extended_color(numbers):
    n = numbers.pop(0)
    if n == 2 and len(numbers) >= 3:
        # 24-bit RGB
        r = numbers.pop(0)
        g = numbers.pop(0)
        b = numbers.pop(0)
        if not all(0 <= c <= 255 for c in (r, g, b)):
            raise ValueError()
    elif n == 5 and len(numbers) >= 1:
        # 256 colors
        idx = numbers.pop(0)
        if idx < 0:
            raise ValueError()
        elif idx < 16:
            # 8 default terminal colors
            return idx % 8  # ignore bright/non-bright distinction
        elif idx < 232:
            # 6x6x6 color cube, see http://stackoverflow.com/a/27165165/500098
            r = (idx - 16) // 36
            r = 55 + r * 40 if r > 0 else 0
            g = ((idx - 16) % 36) // 6
            g = 55 + g * 40 if g > 0 else 0
            b = (idx - 16) % 6
            b = 55 + b * 40 if b > 0 else 0
        elif idx < 256:
            # grayscale, see http://stackoverflow.com/a/27165165/500098
            r = g = b = (idx - 232) * 10 + 8
        else:
            raise ValueError()
    else:
        raise ValueError()
    return r, g, b
