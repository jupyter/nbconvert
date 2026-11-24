"""Tests for conversions from markdown to other formats"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import re
from copy import copy
from functools import partial
from html import unescape
from unittest import skipIf

from jinja2 import Environment

from nbconvert.filters.markdown import markdown2html
from nbconvert.filters.markdown_mistune import MISTUNE_V3
from nbconvert.filters.pandoc import convert_pandoc
from tests.base import TestsBase
from tests.testutils import onlyif_cmds_exist


class TestMarkdown(TestsBase):
    tests = [
        "*test",
        "**test",
        "*test*",
        "_test_",
        "__test__",
        "__*test*__",
        "**test**",
        "#test",
        "##test",
        "test\n----",
        "test [link](https://google.com/)",
    ]

    tokens = [
        "*test",
        "**test",
        "test",
        "test",
        "test",
        "test",
        "test",
        "test",
        "test",
        "test",
        ("test", "https://google.com/"),
    ]

    @onlyif_cmds_exist("pandoc")
    def test_markdown2latex(self):
        """markdown2latex test"""
        for index, test in enumerate(self.tests):
            self._try_markdown(
                partial(convert_pandoc, from_format="markdown", to_format="latex"),
                test,
                self.tokens[index],
            )

    @onlyif_cmds_exist("pandoc")
    def test_markdown2latex_markup(self):
        """markdown2latex with markup kwarg test"""
        # This string should be passed through unaltered with pandoc's
        # markdown_strict reader
        s = "1) arabic number with parenthesis"
        self.assertEqual(convert_pandoc(s, "markdown_strict", "latex"), s)
        # This string should be passed through unaltered with pandoc's
        # markdown_strict+tex_math_dollars reader
        s = r"$\alpha$ latex math"
        # sometimes pandoc uses $math$, sometimes it uses \(math\)
        expected = re.compile(r"(\$|\\\()\\alpha(\$|\\\)) latex math")

        assertRegex = self.assertRegex

        assertRegex(convert_pandoc(s, "markdown_strict+tex_math_dollars", "latex"), expected)

    @onlyif_cmds_exist("pandoc")
    def test_pandoc_extra_args(self):
        # pass --no-wrap
        s = "\n".join(
            [
                "#latex {{long_line | md2l(['--wrap=none'])}}",
                "#rst {{long_line | md2r(['--columns', '5'])}}",
            ]
        )
        long_line = " ".join(["long"] * 30)
        env = Environment()  # noqa
        env.filters.update(
            {
                "md2l": lambda code, extra_args: convert_pandoc(
                    code, from_format="markdown", to_format="latex", extra_args=extra_args
                ),
                "md2r": lambda code, extra_args: convert_pandoc(
                    code, from_format="markdown", to_format="rst", extra_args=extra_args
                ),
            }
        )
        tpl = env.from_string(s)
        rendered = tpl.render(long_line=long_line)
        _, latex, rst = rendered.split("#")

        self.assertEqual(latex.strip(), "latex %s" % long_line)
        self.assertEqual(rst.strip(), "rst %s" % long_line.replace(" ", "\n"))

    def test_markdown2html(self):
        """markdown2html test"""
        for index, test in enumerate(self.tests):
            self._try_markdown(markdown2html, test, self.tokens[index])

    def test_markdown2html_heading_anchors(self):
        for md, tokens in [
            (
                "# test title",
                ("<h1", ">test title", 'id="test-title"', "&#182;</a>", "anchor-link"),
            ),
            (
                "###test head space",
                ("<h3", ">test head space", 'id="test-head-space"', "&#182;</a>", "anchor-link"),
            ),
        ]:
            self._try_markdown(markdown2html, md, tokens)

    def test_markdown2html_math(self):
        # Mathematical expressions not containing <, >, &
        # should be passed through unaltered
        # all the "<", ">", "&" must be escaped correctly
        cases = [
            (
                "\\begin{equation*}\n"
                + (
                    "\\left( \\sum_{k=1}^n a_k b_k \\right)^2 "
                    "\\leq \\left( \\sum_{k=1}^n a_k^2 \\right) "
                    "\\left( \\sum_{k=1}^n b_k^2 \\right)\n"
                )
                + "\\end{equation*}"
            ),
            ("$$\na = 1 *3* 5\n$$"),
            "$ a = 1 *3* 5 $",
            "$s_i = s_{i}\n$",
            "$a<b&b<lt$",
            "$a<b&lt;b>a;a-b<0$",
            "$<k'>$",
            "$$a<b&b<lt$$",
            "$$a<b&lt;b>a;a-b<0$$",
            "$$<k'>$$",
            ("$$x\n=\n2$$"),
            ("$$\nb =  \\left[\nP\\left(\\right)\n- (l_1\\leftrightarrow l_2\n)\\right]\n$$"),
            ("\\begin{equation*}\nx = 2 *55* 7\n\\end{equation*}"),
            """$
\\begin{tabular}{ l c r }
  1 & 2 & 3 \\
  4 & 5 & 6 \\
  7 & 8 & 9 \\
\\end{tabular}$""",
        ]

        for case in cases:
            result = markdown2html(case)
            # find the equation in the generated texts
            search_result = re.search(r"\$.*\$", result, re.DOTALL)
            if search_result is None:
                search_result = re.search(
                    "\\\\begin\\{equation.*\\}.*\\\\end\\{equation.*\\}", result, re.DOTALL
                )
            math = search_result.group(0)  # type:ignore
            # the resulting math part can not contain "<", ">" or
            # "&" not followed by "lt;", "gt;", or "amp;".
            self.assertNotIn("<", math)
            self.assertNotIn(">", math)
            self.assertNotRegex(math, "&(?![gt;|lt;|amp;])")
            # the result should be able to be unescaped correctly
            self.assertEqual(case, unescape(math))

    def test_markdown2html_math_mixed(self):
        """ensure markdown between inline and inline-block math works and
        test multiple LaTeX markup syntaxes.
        """
        case = """The entries of \\\\(C\\\\) are given by the exact formula:
$$
C_{ik} = \\sum_{j=1}^n A_{ij} B_{jk},
$$
but you can _implement_ this computation in many ways.
$\approx 2mnp$ flops are needed for \\\\[ C_{ik} = \\sum_{j=1}^n A_{ij} B_{jk} \\\\].
Also check empty math blocks work correctly:
$$$$
\\\\[\\\\]"""
        output_check = (
            case.replace("_implement_", "<em>implement</em>")
            .replace("\\\\(", "$")
            .replace("\\\\)", "$")
            .replace("\\\\[", "$$")
            .replace("\\\\]", "$$")
        )
        # these replacements are needed because we use $ and $$ in our html output
        self._try_markdown(markdown2html, case, output_check)

    def test_markdown2html_math_paragraph(self):
        """these should all parse without modification"""
        cases = [
            # https://github.com/ipython/ipython/issues/6724
            """Water that is stored in $t$, $s_t$, must equal the storage content of the previous stage,
$s_{t-1}$, plus a stochastic inflow, $I_t$, minus what is being released in $t$, $r_t$.
With $s_0$ defined as the initial storage content in $t=1$, we have""",
            # https://github.com/jupyter/nbviewer/issues/420
            """$C_{ik}$
$$
C_{ik} = \\sum_{j=1}
$$
$C_{ik}$""",
            """$m$
$$
C = \begin{pmatrix}
          0 & 0 & 0 & \\cdots & 0 & 0 & -c_0 \\
          0 & 0 & 0 & \\cdots & 0 & 1 & -c_{m-1}
    \\end{pmatrix}
$$
$x^m$""",
            """$r=\\overline{1,n}$
$$ {\bf
b}_{i}^{r}(t)=(1-t)\\,{\bf b}_{i}^{r-1}(t)+t\\,{\bf b}_{i+1}^{r-1}(t),\\:
 i=\\overline{0,n-r}, $$
i.e. the $i^{th}$""",
        ]

        for case in cases:
            s = markdown2html(case)
            self.assertIn(case, unescape(s))

    def test_markdown2html_keeps_list_markers_inside_display_math(self):
        math_paragraph = "where\n$$\na +\n- b\n$$"
        rendered = markdown2html(f"{math_paragraph}\n\n- a real list item")

        self.assertIn(math_paragraph, unescape(rendered))
        self.assertEqual(rendered.count("<li>"), 1)
        self.assertIn("<li>a real list item</li>", rendered)

    def test_markdown2html_keeps_list_between_display_math_blocks(self):
        rendered = markdown2html("where\n$$\na + b\n$$\n- a real list item\n$$\nc + d\n$$")

        self.assertIn("<li>a real list item", rendered)

    @skipIf(MISTUNE_V3, "Preserves Mistune 2 fenced code parsing")
    def test_markdown2html_unpaired_math_preserves_code_fences(self):
        cases = [
            ("where\n$$\na\n```text\n$$x$$\n```", "$$x$$"),
            ("where\n$$\na\n```text\nliteral\n```\n$$", "literal"),
            ("where\n$$\n- real\n```text\n$$x$$\n```", "$$x$$"),
        ]
        for source, code in cases:
            with self.subTest(source=source):
                rendered = markdown2html(source)
                self.assertRegex(rendered, rf"<pre>[^\n]*{re.escape(code)}\n</pre>")
                self.assertEqual(rendered.count("<li>"), source.count("\n- "))

    @skipIf(MISTUNE_V3, "Preserves Mistune 2 inline code and list parsing")
    def test_markdown2html_inline_code_delimiters_do_not_hide_lists(self):
        cases = [
            ("where\n`code\n$$`\n- real\n$$\n- other", "code $$"),
            ("where\n`code\n$$\n`\n- real\n$$\n- other", "code $$"),
            ("where\n$$\n- real\n`code\n$$\n`", "code $$"),
            ("where\n`code\n-option\n$$`\n- real\n$$\n- other", "code -option $$"),
            ("# Intro `\nwhere\n`code\n-option\n$$`\n- real\n$$\n- other", "code -option $$"),
        ]
        for source, code in cases:
            with self.subTest(source=source):
                rendered = markdown2html(source)
                self.assertIn(f"<code>{code}</code>", rendered)
                self.assertIn("<li>real</li>", rendered)
                self.assertEqual(rendered.count("<li>"), source.count("\n- "))

    @onlyif_cmds_exist("pandoc")
    def test_markdown2rst(self):
        """markdown2rst test"""

        # Modify token array for rst, escape asterisk
        tokens = copy(self.tokens)
        tokens[0] = r"\*test"
        tokens[1] = r"\**test"

        for index, test in enumerate(self.tests):
            self._try_markdown(
                partial(convert_pandoc, from_format="markdown", to_format="rst"),
                test,
                tokens[index],
            )

    def test_mermaid_markdown(self):
        code = """flowchart LR
            chicken --> egg --> chicken"""
        case = f"""```mermaid\n  {code}\n```"""

        output_check = (
            """<div class="jp-Mermaid"><pre class="mermaid">\n"""
            f"""{code.strip()}"""
            """\n</pre></div>"""
        )

        self._try_markdown(markdown2html, case, output_check)

    def _try_markdown(self, method, test, tokens):
        results = method(test)
        if isinstance(tokens, (str,)):
            self.assertIn(tokens, results)
        else:
            for token in tokens:
                self.assertIn(token, results)
