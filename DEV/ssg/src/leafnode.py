from htmlnode import HtmlNode


class LeafNode(HtmlNode):
    def __init__(
        self,
        tag,
        value,
        props,
    ):
        if value is None or value.strip() == "":
            raise ValueError("value cannot be empty")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.tag:
            return self.value
        if not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
