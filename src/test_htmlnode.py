from platform import node
import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_html_node_creation(self):
        node = HTMLNode(tag="div", props={"class": "container"}, value="Hello, World!")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.props, {"class": "container"})
        self.assertEqual(node.value, "Hello, World!")

    def test_html_node_to_string(self):
        node = HTMLNode(tag="span", props={"id": "header"}, value="Welcome to the website.")
        expected_output = '<span id="header">Welcome to the website.</span>'
        self.assertEqual(node.__repr__(), expected_output)

    def test_html_node_to_string2(self):
        node = HTMLNode(tag="div", props={"class": "header"}, value="Div content")
        expected_output = '<div class="header">Div content</div>'
        self.assertEqual(node.__repr__(), expected_output)

    def test_html_node_to_string3(self):
        node = HTMLNode(tag="a", props={"href": "https://www.example.com", "target": "_blank"}, value="Div content")
        expected_output = '<a href="https://www.example.com" target="_blank">Div content</a>'
        self.assertEqual(node.__repr__(), expected_output)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p2(self):
        node = LeafNode("p", "Hello, world!", {"class": "container"})
        self.assertEqual(node.to_html(), '<p class="container">Hello, world!</p>')

    def test_leaf_to_html_text(self):
        node = LeafNode("", "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


class TestParentNode(unittest.TestCase):
    def test_to_html_without_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_without_tag(self):
        parent_node = ParentNode(None, [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

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

    def test_from_lesson(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, " Normal text "),
                LeafNode("i", "italic text"),
                LeafNode(None, " Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b> Normal text <i>italic text</i> Normal text</p>")

    def test_from_lesson2(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text", {"class": "bold"}),
                LeafNode(None, " Normal text "),
                LeafNode("i", "italic text"),
                LeafNode(None, " Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b class=\"bold\">Bold text</b> Normal text <i>italic text</i> Normal text</p>")
        

class TestTextToLeafNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is an anchor tag", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is an anchor tag")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "https://www.example.com", "alt": "This is an image node"})


if __name__ == "__main__":
    unittest.main()