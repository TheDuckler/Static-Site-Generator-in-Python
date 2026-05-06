import sys

from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from extractmarkdown import extract_markdown_images, extract_markdown_links


def main():
	node = TextNode("this is text", TextType.LINK, "this is url")
	message = node.__repr__()
	print(message)


main()
