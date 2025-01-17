import re
from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def text_node_to_html_node(self):
        match (self.text_type):
            case TextType.TEXT:
                return LeafNode(None, self.text, {})
            case TextType.BOLD:
                return LeafNode("b", self.text, {})
            case TextType.ITALIC:
                return LeafNode("i", self.text, {})
            case TextType.CODE:
                return LeafNode("code", self.text, {})
            case TextType.LINK:
                return LeafNode("a", self.text, {"href": f"{self.url}"})
            case TextType.IMAGE:
                return LeafNode(
                    "img", self.url, {"src": f"{self.text}", "alt": f"{self.url}"}
                )


def split_nodes_image(nodes):
    result = []
    for node in nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            result.append(node)
            continue
        text = node.text
        for image in images:
            parts = text.split(f"![{image[0]}]({image[1]})", 1)
            if parts[0] != "":
                result.append(TextNode(parts[0], TextType.TEXT))
            result.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = parts[1]
        if text != "":
            result.append(TextNode(text, TextType.TEXT))
    return result


def split_nodes_link(nodes):
    result = []
    for node in nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            result.append(node)
            continue
        text = node.text
        for link in links:
            parts = text.split(f"[{link[0]}]({link[1]})", 1)
            if parts[0] != "":
                result.append(TextNode(parts[0], TextType.TEXT))
            result.append(TextNode(link[0], TextType.LINK, link[1]))
            text = parts[1]
        if text != "":
            result.append(TextNode(text, TextType.TEXT))
    return result


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if not node.text or not node.text.strip():
            continue
        if node.text_type != TextType.TEXT:
            result.append(node)
        else:
            split_parts = []
            if delimiter == "*":
                split_parts = list(re.split(r"(?<!\*)\*(?!\*)", node.text))
            else:
                split_parts = list(node.text.split(delimiter))
            if len(split_parts) % 2 == 0:
                raise Exception("invalid markdown syntax")
            toggle = False
            while len(split_parts) > 0:
                result.append(
                    TextNode(split_parts[0], text_type if toggle else TextType.TEXT)
                )
                split_parts = split_parts[1:]
                toggle = not toggle
    return result


def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images


def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links


def text_to_textnodes(text):
    text_node = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_link(text_node)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    return nodes
