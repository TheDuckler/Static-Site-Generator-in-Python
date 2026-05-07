import unittest

from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node
from textnode import TextType, TextNode


class TestSplitNodeDelimiter(unittest.TestCase):
####SPLIT NODE DELIMITER TESTS
    def test_split_nodes_delimiter_eq1(self):
        node = split_nodes_delimiter([TextNode("This is text with a 'code block' word", TextType.PLAIN)], "'", TextType.CODE)
        node2 = [TextNode("This is text with a ", TextType.PLAIN), TextNode("code block", TextType.CODE), TextNode(" word", TextType.PLAIN)]
        self.assertEqual(node, node2)

    def test_split_nodes_delimiter_except1(self):
        with self.assertRaises(Exception):
            split_nodes_delimiter([TextNode("This is text with a 'code block word", TextType.PLAIN)], "'", TextType.CODE)

    def test_split_nodes_delimiter_except2(self):
        with self.assertRaises(Exception):
            split_nodes_delimiter([TextNode("This is' text with a 'code blo'ck word", TextType.PLAIN)], "'", TextType.CODE)

    def test_split_nodes_delimiter_eq2(self):
        node = split_nodes_delimiter([TextNode("This is text ?with? a ?code block? word", TextType.PLAIN)], "?", TextType.BOLD)
        node2 = [TextNode("This is text ", TextType.PLAIN), TextNode("with", TextType.BOLD), TextNode(" a ", TextType.PLAIN), TextNode("code block", TextType.BOLD), TextNode(" word", TextType.PLAIN)]
        self.assertEqual(node, node2)

    def test_split_nodes_delimiter_not_eq1(self):
        node = split_nodes_delimiter([TextNode("This is text ?with? a ?code block? word", TextType.PLAIN)], "?", TextType.BOLD)
        node2 = [TextNode("This is text ", TextType.PLAIN), TextNode("with", TextType.CODE), TextNode(" a ", TextType.PLAIN), TextNode("code block", TextType.CODE), TextNode(" word", TextType.PLAIN)]
        self.assertNotEqual(node, node2)


####SPLIT NODE IMAGE TESTS
    def test_split_images_eq1(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_eq2(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![stupid chud",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ![stupid chud", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_images_not_eq1(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertNotEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.PLAIN),
            ],
            new_nodes,
        )


####SPLIT NODE LINK TESTS
    def test_split_links_eq1(self):
        node = TextNode(
            "This is text with an [link](https://www.boot.dev) and another [second link](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_eq2(self):
        node = TextNode(
            "This is text with an [link](https://www.boot.dev) and another [sebudds bingev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another [sebudds bingev)", TextType.PLAIN),
            ],
            new_nodes,
        )


####TEXT TO TEXTNODES TESTS
    def test_text_to_textnodes_eq1(self):
        node = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        node2 = [
                    TextNode("This is ", TextType.PLAIN),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.PLAIN),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.PLAIN),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.PLAIN),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.PLAIN),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ]
        self.assertEqual(node, node2)


    def test_text_to_textnodes_eq2(self):
        node = text_to_textnodes("This is **text** with another **bold** word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [linkps://boot.dev)")
        node2 = [
                    TextNode("This is ", TextType.PLAIN),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with another ", TextType.PLAIN),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" word and a ", TextType.PLAIN),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.PLAIN),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a [linkps://boot.dev)", TextType.PLAIN),
                ]
        self.assertEqual(node, node2)

    def test_text_to_textnodes_not_eq1(self):
        node = text_to_textnodes("This is **text** with an _italic_ bumbd an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        node2 = [
                    TextNode("This is ", TextType.PLAIN),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.PLAIN),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" bumbum and an ", TextType.PLAIN),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.PLAIN),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ]
        self.assertNotEqual(node, node2)

    def test_text_to_textnodes_all_links_and_images1(self):
        with self.assertRaises(Exception):
            node = text_to_textnodes("[This is **text*](* with an _italic_) [word and]( a code block`) ![and]( an) ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)[ and]() a) [link](https://boot.dev)")
            
    def test_text_to_textnodes_eq3(self):
        node = text_to_textnodes("This is *text* with an _italic_ word and a `code block` and `an `![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        node2 = [
                    TextNode("This is *text* with an ", TextType.PLAIN),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.PLAIN),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and ", TextType.PLAIN),
                    TextNode("an ", TextType.CODE),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.PLAIN),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ]
        self.assertEqual(node, node2)


####TEST FOR MARKDOWN TO BLOCKS
    def test_markdown_to_blocks_eq1(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
        ],
    )

    def test_markdown_to_blocks_not_eq1(self):
        md = """
This is **bolded** paragraph

This is another paragraic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertNotEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
        ],
    )
        
    def test_markdown_to_blocks_eq2(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
HEY, IM WALKIN' 'ERE!!!
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nHEY, IM WALKIN' 'ERE!!!\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
        ],
    )
        
    def test_markdown_to_blocks_eq3(self):
        md = """
This is **bolded** paragraph

- This is a seperate list
- with 3 lines
- here's the third

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "- This is a seperate list\n- with 3 lines\n- here's the third",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
        ],
    )
        
    def test_markdown_to_blocks_eq4(self):
        md = """
# Heading Alert!!

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading Alert!!",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
        ],
    )


####TEST FOR BLOCK TO BLOCK TYPE
    def test_block_to_block_type_eq1(self):
        block = "# Heading Alert!!"
        self.assertEqual(block_to_block_type(block), BlockType.HEADINGS)

    def test_block_to_block_type_eq2(self):
        block = "```\nThis is a code block\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE_BLOCKS)

    def test_block_to_block_type_eq3(self):
        block = "> This is a quote block"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE_BLOCKS)

    def test_block_to_block_type_eq4(self):
        block = "- This is an unordered list item\n- This is another unordered list item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LISTS)

    def test_block_to_block_type_eq5(self):
        block = "1. This is an ordered list item\n2. This is another ordered list item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LISTS)


####TEST MARKDOWN TO HTML NODE
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )
        
    def test_quote_block(self):
        md = """
    > This is a quote block
    > with multiple lines

    > and some **inline** stuff that _should_ be parsed

    """
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote block\nwith multiple lines</blockquote><blockquote>and some <b>inline</b> stuff that <i>should</i> be parsed</blockquote></div>",
        )

    def test_heading_and_lists(self):
        md = """
    ## Heading Alert!!

    - Here is a list
    - with multiple items
    - and some **bold** text

    """
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Heading Alert!!</h2><ul><li>Here is a list</li><li>with multiple items</li><li>and some <b>bold</b> text</li></ul></div>",
        )


    def test_heading_and_orderred_lists(self):
        md = """
    ## Heading Alert!!

    1. Here is a list
    2. with multiple items
    3. and some **bold** text

    """
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Heading Alert!!</h2><ol><li>Here is a list</li><li>with multiple items</li><li>and some <b>bold</b> text</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()
