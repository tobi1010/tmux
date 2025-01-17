import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("node", TextType.ITALIC)
        node2 = TextNode("node2", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq(self):
        node = TextNode("node", TextType.CODE, None)
        node2 = TextNode("node", TextType.CODE)
        self.assertEqual(node, node2)

    def img_text_to_html(self):
        node = TextNode("URL", TextType.IMG, "altText")
        self.assertEqual(
            node.text_node_to_html(), '<img src="URL" alt="altText"></img>'
        )

    def link_text_to_html(self):
        node = TextNode("text", TextType.LINK, "URL")
        self.assertEqual(node.text_node_to_html(), '<a> href="URL">text</a>')

    def normal_text_to_html(self):
        node = TextNode("text", TextType.TEXT, {})
        self.assertEqual(node.text_node_to_html(), "text")

    def italic_text_to_html(self):
        node = TextNode("text", TextType.ITALIC, {})
        self.assertEqual(node.text_node_to_html(), "<i>text</i>")

    def bold_text_to_html(self):
        node = TextNode("text", TextType.BOLD, {})
        self.assertEqual(node.text_node_to_html(), "<b>text</b>")

    def code_text_to_html(self):
        node = TextNode("text", TextType.CODE, {})
        self.assertEqual(node.text_node_to_html(), "<code>text</code>")


if __name__ == "__main__":
    unittest.main()
