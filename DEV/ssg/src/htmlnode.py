class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        if isinstance(children, list):
            self.children = children
        else:
            self.children = None
        if isinstance(props, dict):
            self.props = props
        else:
            self.props = None

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        props_strings = []
        for key, val in self.props.items():
            props_strings.append(f'{key}="{val}"')
        return " ".join(props_strings)

    def __eq__(self, other):
        return (
            isinstance(other, HtmlNode)
            and self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        return f"tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}"
