import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
####HTMLNODE TESTS
    def test_eq1(self):
        node = HTMLNode("tag", "value", ["child"], {"swag": "bucks.com"})
        node2 = HTMLNode("tag", "value", ["child"], {"swag": "bucks.com"})
        self.assertEqual(node, node2)

    def test_not_eq1(self):
        node = HTMLNode("tag", "value", ["child"], {"swag": "bucks.com"})
        node2 = HTMLNode("tag", "value", None, {"swag": "bucks.com"})
        self.assertNotEqual(node, node2)

    def test_eq2(self):
        node = HTMLNode("tag", "value")
        node2 = HTMLNode("tag", "value")
        self.assertEqual(node, node2)

    def test_eq3(self):
        node = HTMLNode("tag", None, ["child"], {"swag": "bucks.com", "shoot": "ropes.com"})
        node2 = HTMLNode("tag", None, ["child"], {"swag": "bucks.com", "shoot": "ropes.com"})
        self.assertEqual(node, node2)

    def test_prop_to(self):
        node = HTMLNode("tag", None, ["child"], {"swag": "bucks.com", "shoot": "ropes.com"}).props_to_html()
        node2 = " swag='bucks.com' shoot='ropes.com'"
        self.assertEqual(node, node2)

####LEAFNODE TESTS
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_lef_eq1(self):
        node = LeafNode("p", "Hello, world!", {"swag": "bucks.com"})
        self.assertEqual(node.to_html(), "<p swag='bucks.com'>Hello, world!</p>")

    def test_lef_not_eq1(self):
        node = LeafNode("p", "Hello, world!", {"swag": "bucks.com"})
        self.assertNotEqual(node.to_html(), "<p swag='bucks.com'>BAZINGA!</p>")

    def test_lef_eq2(self):
        node = LeafNode("p", "Hello, world!", {"swag": "bucks.com", "shoot": "ropes.com"})
        self.assertEqual(node.to_html(), "<p swag='bucks.com' shoot='ropes.com'>Hello, world!</p>")

    def test_lef_eq3(self):
        node = LeafNode("z", "I love links <3", {"swag": "bucks.com"})
        self.assertEqual(node.to_html(), "<z swag='bucks.com'>I love links <3</z>")

####PARENTNODE TESTS
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )
        
    def test_to_html_with_2children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child1</span><span>child2</span></div>",
    )

    def test_to_html_with_no_children(self):
        child_node = ParentNode("span", [])
        parent_node = ParentNode("div", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_complex_child(self):
        child_node = LeafNode("span", "child", {"class": "my-class"})
        parent_node = ParentNode("div", [child_node], {"id": "my-id"})
        self.assertEqual(
            parent_node.to_html(),
            "<div id='my-id'><span class='my-class'>child</span></div>",
    )


if __name__ == "__main__":
    unittest.main()
