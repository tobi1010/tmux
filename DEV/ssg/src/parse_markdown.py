import re

from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_to_textnodes


def markdown_to_blocks(markdown):
    blocks = []
    lines = markdown.split("\n")
    block = []
    for line in lines:
        line = line.strip()
        if line != "":
            block.append(line)
        else:
            blocks.append("\n".join(block))
            block = []
    if block:
        blocks.append("\n".join(block))
    return blocks


def block_to_block_type(block):
    regex_heading = r"^#{1,6} \S.*$"
    regex_code = r"^```[\s\S]*?```$"
    regex_quote = r"^>.*$"
    regex_ulist = r"^([-*] .*\n)+"
    regex_olist = r"^(\d+\. .*\n)+"
    if re.match(regex_heading, block):
        return "heading"
    if re.match(regex_code, block):
        return "code"
    if re.match(regex_quote, block):
        return "quote"
    if re.match(regex_ulist, block):
        return "unordered_list"
    if re.match(regex_olist, block):
        if is_valid_order(block):
            return "ordered_list"
    return "paragraph"


def is_valid_order(block):
    lines = block.split("\n")
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i+1}"):
            return False
    return True


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case "heading":
                level = get_heading_level(block)
                text = get_text_from_block(block, "heading")
                children.append(ParentNode(f"h{level}", text_to_children(text)))
            case "code":
                code_text = get_text_from_block(block, "code")
                code_child = LeafNode("code", code_text, {})
                code_node = ParentNode("pre", [code_child])
                children.append(code_node)
            case "quote":
                quote_text = get_text_from_block(block, "quote")
                children.append(ParentNode("blockquote", text_to_children(quote_text)))
            case "unordered_list":
                items = process_list(block, "unordered_list")
                children.append(ParentNode("ul", items))
            case "ordered_list":
                items = process_list(block, "ordered_list")
                children.append(ParentNode("ol", items))
            case "paragraph":
                children.append(ParentNode("p", text_to_children(block)))
    return ParentNode("div", children)


def get_text_from_block(block, type):
    text = ""
    match type:
        case "heading":
            text = re.sub(r"^#{1,6}", "", block).strip()
        case "code":
            text = re.sub(r"```", "", block).strip()
        case "quote":
            text = re.sub(r"^>\s*", "", block).strip()
    return text


def get_heading_level(block):
    match = re.match(r"^(#{1,6})", block)
    return len(match.group(1))


def process_list(block, type):
    items = []
    match type:
        case "unordered_list":
            lines = block.split("\n")
            for line in lines:
                line = re.sub(r"[-*]", "", line).strip()
                items.append(ParentNode("li", text_to_children(line)))
        case "ordered_list":
            lines = block.split("\n")
            for line in lines:
                line = re.sub(r"\d+\.", "", line).strip()
                items.append(ParentNode("li", text_to_children(line)))
    return items


def text_to_children(text):
    print(f"Processing text to children: '{text}'")
    html_nodes = []
    nodes = text_to_textnodes(text)
    for node in nodes:
        if node.text and node.text.strip():
            html_node = node.text_node_to_html_node()
            if html_node:
                html_nodes.append(html_node)
    return html_nodes
