import unittest

from htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HtmlNode()
        node2 = HtmlNode()
        self.assertEqual(node, node2)

    def test_default(self):
        node = HtmlNode("div", "hello", "wrong", "arguments")
        node2 = HtmlNode("div", "hello")
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HtmlNode("div", "hello", [], {"key1": "val1", "key2": "val2"})
        self.assertEqual(node.props_to_html(), 'key1="val1" key2="val2"')


if __name__ == "__main__":
    unittest.main()
