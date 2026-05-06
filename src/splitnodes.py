from textnode import TextType, TextNode
from extractmarkdown import extract_markdown_images, extract_markdown_links
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception("closing delimiter not found")
        
        t = 0
        for text in split_text:
            t += 1
            if t % 2 != 0:
                new_nodes.append(TextNode(text, TextType.PLAIN))
            else:
                new_nodes.append(TextNode(text, text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        og_text = node.text
        matches = extract_markdown_images(og_text)
        
        if len(matches) == 0:
            new_nodes.append(node)
            continue

        for match in matches:
            sections = og_text.split(f"![{match[0]}]({match[1]})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN))

            new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            og_text = sections[1]

        if og_text != "":
            new_nodes.append(TextNode(og_text, TextType.PLAIN))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        og_text = node.text
        matches = extract_markdown_links(og_text)
        
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        for match in matches:
            sections = og_text.split(f"[{match[0]}]({match[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN))
            new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            og_text = sections[1]
        if og_text != "":
            new_nodes.append(TextNode(og_text, TextType.PLAIN))

    return new_nodes


def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.PLAIN)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)

    return new_nodes
