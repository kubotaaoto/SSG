from enum import Enum
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_children
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

class BlockNode:
    def __init__(self, text, block_type):
        self.text = text
        self.block_type = block_type

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = BlockNode(block, block_type)
        html_node = block_node_to_html_node(block_node)
        children.append(html_node)
    return ParentNode("div", children)


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    res = []
    for block in blocks:
        block = block.strip()
        if block != "":
            res.append(block)
    return res

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def block_node_to_html_node(block_node):
    text = block_node.text
    type = block_node.block_type
    match type:
        case BlockType.PARAGRAPH:
            lines = text.split("\n")
            paragraph = " ".join(lines)
            return ParentNode("p", text_to_children(paragraph))
        case BlockType.HEADING:
            if text.startswith("# "):
                return ParentNode("h1", text_to_children(text[2:]))
            if text.startswith("## "):
                return ParentNode("h2", text_to_children(text[3:]))
            if text.startswith("### "):
                return ParentNode("h3", text_to_children(text[4:]))
            if text.startswith("#### "):
                return ParentNode("h4", text_to_children(text[5:]))
            if text.startswith("##### "):
                return ParentNode("h5", text_to_children(text[6:]))
            if text.startswith("###### "):
                return ParentNode("h6", text_to_children(text[7:]))
        case BlockType.QUOTE:
            lines = text.split("\n")
            new_lines = []
            for line in lines:
                new_lines.append(line.lstrip(">").strip())
            content = " ".join(new_lines)
            return ParentNode("blockquote", text_to_children(content))
        case BlockType.CODE:
            text = text[4:-3]
            leafnode = text_node_to_html_node(TextNode(text, TextType.TEXT))
            code_html = ParentNode("code", [leafnode])
            return ParentNode("pre", [code_html])
        case BlockType.ULIST:
            return list_block_to_list_html(type, text)
        case BlockType.OLIST:
            return list_block_to_list_html(type, text)
        case _:
            ValueError(f"invalid block type: {type}")

def list_block_to_list_html(list_type, text):
    if list_type not in (BlockType.ULIST, BlockType.OLIST):
        raise ValueError(f"not a list type: {list_type}")
    lines = text.split("\n")
    children = []
    if list_type == BlockType.ULIST:
        for line in lines:
            children.append(ParentNode("li", text_to_children(line[2:])))
        return ParentNode("ul", children)
    else:
        for line in lines:
            children.append(ParentNode("li", text_to_children(line[3:])))
        return ParentNode("ol", children)
