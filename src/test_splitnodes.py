import unittest

from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
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


if __name__ == "__main__":
    unittest.main()
