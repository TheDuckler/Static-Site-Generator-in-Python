import textwrap

from enum import Enum

from textnode import TextType, TextNode, text_node_to_html_node
from extractmarkdown import extract_markdown_images, extract_markdown_links
from htmlnode import HTMLNode, LeafNode, ParentNode
#import re


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


def markdown_to_blocks(markdown):
    block_strings = []

    split_strings = markdown.split('\n\n')
    for string in split_strings:
        stripped_string = string.strip()
        if stripped_string != "":
            block_strings.append(stripped_string)

    return block_strings


class BlockType(Enum):
    HEADINGS = "headings"
    CODE_BLOCKS = "code_blocks"
    QUOTE_BLOCKS = "quote_blocks"
    UNORDERED_LISTS = "unordered_lists"
    ORDERED_LISTS = "ordered_lists"
    PARAGRAPHS = "paragraphs"


def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADINGS
    
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE_BLOCKS
    
    elif block.startswith(">"):
        return BlockType.QUOTE_BLOCKS
    
    elif block.startswith("- "):
        return BlockType.UNORDERED_LISTS
    
    elif block[0].isdigit() and block[1:3] == ". ":
        return BlockType.ORDERED_LISTS
    
    else:
        return BlockType.PARAGRAPHS
    

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    #print("TEXT:", repr(text)) #Test for Error Placement#
    html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
    return html_nodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADINGS:
            heading_level = block.split(" ")[0].count("#")
            html_nodes.append(ParentNode(f"h{heading_level}", text_to_children(block[heading_level + 1:].strip())))

        elif block_type == BlockType.CODE_BLOCKS:
            code = block.removesuffix("```").removeprefix("```\n")
            dedented_code = textwrap.dedent(code)
            html_nodes.append(ParentNode("pre", [LeafNode("code", dedented_code, None)]))

        elif block_type == BlockType.QUOTE_BLOCKS:
            split_block = block.split("\n")
            cleaned = []
            for line in split_block:
                line = line.strip()
                cleaned_line = line.removeprefix(">").strip()
                cleaned.append(cleaned_line)
            quote = "\n".join(cleaned)
            html_nodes.append(ParentNode("blockquote", text_to_children(quote)))

        elif block_type == BlockType.UNORDERED_LISTS:
            lines = block.split("\n")
            list_items = []
            list_item = 0
            for item in lines:
                if list_item == 0:
                    list_items.append(item[2:].strip())
                    list_item += 1
                else:
                    list_items.append(item[2:].strip())
            html_nodes.append(ParentNode("ul", [ParentNode("li", text_to_children(item.strip())) for item in list_items]))

        elif block_type == BlockType.ORDERED_LISTS:
            split_block = block.split("\n")
            list_items = []
            for item in split_block:
                splitted = item.split(". ", 1)
                list_items.append(splitted[1].strip())
            html_nodes.append(ParentNode("ol", [ParentNode("li", text_to_children(item)) for item in list_items]))
        
        elif block_type == BlockType.PARAGRAPHS:
            lines = block.split("\n")
            cleaned_lines = []
            for line in lines:
                cleaned_lines.append(line.strip())

            paragraph_text = " ".join(cleaned_lines)
            html_nodes.append(ParentNode("p", text_to_children(paragraph_text)))


    parent_HTMLNode = ParentNode("div", html_nodes)
    return parent_HTMLNode
