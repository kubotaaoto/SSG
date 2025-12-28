from textnode import TextType, TextNode, text_node_to_html_node
import re

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    leafnodes = []
    for textnode in textnodes:
        leafnodes.append(text_node_to_html_node(textnode))
    return leafnodes

def text_to_textnodes(text):
    parent_textnode = TextNode(text, TextType.TEXT)
    bold_done = split_nodes_delimiter([parent_textnode], "**", TextType.BOLD)
    italic_done = split_nodes_delimiter(bold_done, "_", TextType.ITALIC)
    code_done = split_nodes_delimiter(italic_done, "`", TextType.CODE)
    image_done = split_nodes_image(code_done)
    link_done = split_nodes_link(image_done)
    return link_done

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        matches = extract_markdown_images(text)
        for match in matches:
            image_alt, image_url = match[0], match[1]
            sections = text.split(f"![{image_alt}]({image_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        matches = extract_markdown_links(text)
        for match in matches:
            link_text, link_url = match[0], match[1]
            sections = text.split(f"[{link_text}]({link_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


# def split_nodes_delimiter(old_nodes, delimiter, text_type):
#     res = []
#     for old_node in old_nodes:
#         if old_node.text_type != TextType.TEXT:
#             res.append(old_node)
#             continue
#         full_text = old_node.text
#         start = full_text.find(delimiter)
#         end = full_text.find(delimiter, start + 1)

#         if start == -1 or end == -1:
#             return [TextNode(full_text, TextType.TEXT)]
        
#         if start == 0 and end + len(delimiter) - 1 == len(full_text) - 1:
#             res.append(TextNode(full_text, text_type))
#         elif start == 0:
#             res.append(TextNode(full_text[start+len(delimiter):end], text_type))
#             res.append(TextNode(full_text[end+len(delimiter):], TextType.TEXT))
#         elif end + len(delimiter) - 1 == len(full_text) - 1:
#             res.append(TextNode(full_text[:start], TextType.TEXT))
#             res.append(TextNode(full_text[start+len(delimiter):end], text_type))
#         else:
#             res.append(TextNode(full_text[:start], TextType.TEXT))
#             res.append(TextNode(full_text[start+len(delimiter):end], text_type))
#             res.append(TextNode(full_text[end+len(delimiter):], TextType.TEXT))
    
#     for new_node in res:
#         if new_node not in old_nodes and new_node.text_type == TextType.TEXT:
#             res.extend(split_nodes_delimiter([new_node], delimiter, text_type))
        
#     return res
