from htmlnode import HtmlNode


class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        if not children:
            raise ValueError("children cannot be empty")
        if not tag:
            raise ValueError("tag cannot be empty")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.children:
            raise ValueError("children cannot be empty")
        if not self.tag:
            raise ValueError("tag cannot be empty")
        value = ""
        for child in self.children:
            value += child.to_html()
        return f"<{self.tag}>{value}</{self.tag}>"
