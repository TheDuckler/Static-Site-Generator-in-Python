import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
####TEXTNODE TESTS
    def test_eq1(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq1(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a scrumblo node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.LINK, "cool freaking url")
        node2 = TextNode("This is a text node", TextType.LINK, "cool freaking url")
        self.assertEqual(node, node2)

    def test_not_eq3(self):
        node = TextNode("This is a text node", TextType.BOLD, "cool freaking url")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    
####TEXTNODE TO HTML TESTS
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "cool freaking url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "cool freaking url"})

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "cool freaking url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "cool freaking url", "alt": "This is a text node"})

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.IMAGE, "cool freaking url")
        html_node = text_node_to_html_node(node)
        self.assertNotEqual(html_node.tag, "a")
        self.assertNotEqual(html_node.value, "This is a text node")
        self.assertNotEqual(html_node.props, {"href": "cool freaking url"})


if __name__ == "__main__":
    unittest.main()
