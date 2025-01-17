import unittest

from textnode import TextNode, TextType, split_nodes_image, split_nodes_link


class TestSplitTextNode(unittest.TestCase):
    def test_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_img(self):
        node = TextNode(
            "This is text with an image ![boot dev](https://www.boot.dev) and ![youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("boot dev", TextType.IMAGE, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )


if __name__ == "__main__":
    unittest.main()
