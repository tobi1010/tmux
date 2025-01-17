import unittest

from parse_markdown import markdown_to_html_node


class TestParseMarkdown(unittest.TestCase):
    def md_to_html(self):
        md = """ # Main Title

        This is a regular paragraph with some *italic* and **bold** text.

        ## Second Level Header

        * First item in unordered list
        * Second item
        * Third item

        1. First numbered item
        2. Second numbered item
        3. Third numbered item

        > This is a blockquote
        > It can span multiple lines

        Here's a code block:

        ```python
        def hello_world():
            print("Hello, World!")```"""
        expected = """<div>
        <h1>Main Title</h1>
        <p>This is a regular paragraph with some <em>italic</em> and <strong>bold</strong> text.</p>
        <h2>Second Level Header</h2>
        <ul>
            <li>First item in unordered list</li>
            <li>Second item</li>
            <li>Third item</li>
        </ul>

        <ol>
            <li>First numbered item</li>
            <li>Second numbered item</li>
            <li>Third numbered item</li>
        </ol>
        <blockquote>
            <p>This is a blockquote
            It can span multiple lines</p>
        </blockquote>
        <p>Here's a code block:</p>
        <pre><code>def hello_world():
        print("Hello, World!")</code></pre>
        </div>"""

        self.assertEqual(markdown_to_html_node(md), expected)
