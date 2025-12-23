import unittest

from htmlnode import HTMLNode

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


if __name__ == "__main__":
    unittest.main()