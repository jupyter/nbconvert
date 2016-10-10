"""Tests for the HTMLSanitize preprocessor"""

from .base import PreprocessorTestsBase
from ..sanitize import SanitizeHTML
from nbformat import v4 as nbformat


class TestSanitizer(PreprocessorTestsBase):
    """Contains test functions for sanitize.py"""

    def build_preprocessor(self):
        """Make an instance of a preprocessor"""
        preprocessor = SanitizeHTML()
        preprocessor.enabled = True
        return preprocessor

    def preprocess_source(self, cell_type, source, preprocessor):
        nb = self.build_notebook()
        res = self.build_resources()

        nb.cells[0].cell_type = cell_type
        nb.cells[0].source = source

        nb, res = preprocessor(nb, res)

        return nb.cells[0].source

    def test_constructor(self):
        """Can a SanitizeHTML be constructed?"""
        self.build_preprocessor()

    def test_svg_handling(self):
        """
        Test to make sure that svgs are handled 'properly'

        We do this by only allowing <img> tags (which can not have JS in svgs)
        and not <object> or <embed> tags
        """
        preprocessor = self.build_preprocessor()
        preprocessor.strip = True

        self.assertEqual(
            self.preprocess_source(
                'markdown',
                """
                ![some image](http://example.com/something.svg)
                <object data="something.svg" type="image/svg+xml" />
                <embed data="something.svg" type="image/svg+xml" />
                """,
                preprocessor
            ).strip(),
            """
            ![some image](http://example.com/something.svg)
            """.strip(),
        )

    def test_tag_whitelist_stripping(self):
        """Test tag whitelisting + stripping out offending tags"""
        preprocessor = self.build_preprocessor()
        preprocessor.strip = True

        self.assertEqual(
            self.preprocess_source(
                'markdown',
                '_A_ <em>few</em> <script>tags</script>',
                preprocessor
            ),
            '_A_ <em>few</em> tags'
        )

    def test_comment_stripping(self):
        """Test HTML comment stripping"""
        preprocessor = self.build_preprocessor()

        self.assertEqual(
            self.preprocess_source(
                'markdown',
                '_A_ <em>few</em> <!-- tags -->',
                preprocessor
            ),
            '_A_ <em>few</em> '
        )

        preprocessor.strip_comments = False
        self.assertEqual(
            self.preprocess_source(
                'markdown',
                '_A_ <em>few</em> <!-- tags -->',
                preprocessor
            ),
            '_A_ <em>few</em> <!-- tags -->'
        )

    def test_attributes_whitelist(self):
        """Test style"""
        preprocessor = self.build_preprocessor()

        preprocessor.attributes['a'] = ['href', 'title']

        self.assertEqual(
            self.preprocess_source(
                'markdown',
                '<a href="link" rel="nofollow">Hi</a>',
                preprocessor
            ),
            '<a href="link">Hi</a>'
        )

    def test_style_whitelist(self):
        """Test style"""
        preprocessor = self.build_preprocessor()

        if '*' in preprocessor.attributes:
            preprocessor.attributes['*'].append('style')
        else:
            preprocessor.attributes['*'] = ['style']
        preprocessor.styles = [
            'color',
        ]

        self.assertEqual(
            self.preprocess_source(
                'markdown',
                '_A_ <em style="color: blue; background-color: pink">'
                'few</em> <script>tags</script>',
                preprocessor
            ),
            '_A_ <em style="color: blue;">few</em> '
            '&lt;script&gt;tags&lt;/script&gt;'
        )

    def test_tag_passthrough(self):
        """Test passing through raw output"""
        preprocessor = self.build_preprocessor()

        self.assertEqual(
            self.preprocess_source(
                'raw',
                '_A_ <em>few</em> <script>tags</script>',
                preprocessor
            ),
            '_A_ <em>few</em> &lt;script&gt;tags&lt;/script&gt;'
        )

    def test_output_sanitizing(self):
        """Test that outputs are also sanitized properly"""
        preprocessor = self.build_preprocessor()
        nb = self.build_notebook()

        outputs = [
            nbformat.new_output("display_data", data={
                'text/plain': 'b',
                'text/html': '<script>more evil</script>'
                }),
            nbformat.new_output('stream', name='stdout', text="wat"),
            nbformat.new_output('stream', name='stdout', text="<script>Evil tag</script>")
        ]
        nb.cells[0].outputs = outputs

        res = self.build_resources()
        nb, res = preprocessor(nb, res)

        expected_output = [
            {
                'data': {
                    'text/html': '&lt;script&gt;more evil&lt;/script&gt;',
                    'text/plain': 'b'
                },
                'metadata': {},
                'output_type': 'display_data',
            },
            {
                'name': 'stdout',
                'output_type': 'stream',
                'text': 'wat'
            },
            {
                'name': 'stdout',
                'output_type':
                'stream', 'text': '<script>Evil tag</script>'
            }
        ]
        self.assertEqual(nb.cells[0].outputs, expected_output)

    def test_tag_whitelist(self):
        """Test tag whitelisting"""
        preprocessor = self.build_preprocessor()

        self.assertEqual(
            self.preprocess_source(
                'markdown',
                '_A_ <em>few</em> <script>tags</script>',
                preprocessor
            ),
            '_A_ <em>few</em> &lt;script&gt;tags&lt;/script&gt;'
        )
