import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_eq(self):
        child = LeafNode("p", "This is a paragraph of text.", {})
        parent = ParentNode("div", [child], {})
        self.assertEqual(
            parent.to_html(), "<div><p>This is a paragraph of text.</p></div>"
        )

    def test_eq_nested(self):
        child1 = LeafNode("p", "This is a paragraph of text.", {})
        child2 = ParentNode("div", [child1], {})
        parent = ParentNode("div", [child2], {})
        self.assertEqual(
            parent.to_html(),
            "<div><div><p>This is a paragraph of text.</p></div></div>",
        )

    def test_eq_rec(self):
        child1 = LeafNode("p", "This is a paragraph of text.", {})
        child2 = LeafNode("p", "This is another paragraph of text.", {})
        children = [child1, child2]
        child3 = ParentNode("div", children, {})
        parent = ParentNode("div", [child3], {})
        self.assertEqual(
            parent.to_html(),
            "<div><div><p>This is a paragraph of text.</p><p>This is another paragraph of text.</p></div></div>",
        )


if __name__ == "__main__":
    unittest.main()
