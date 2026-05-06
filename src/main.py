import sys
from textnode import TextType, TextNode
from htmlnode import HTMLNode
from splitnodedelimiter import split_nodes_delimiter


def main():
	node = TextNode("this is text", TextType.LINK, "this is url")
	message = node.__repr__()
	print(message)


main()
