import unittest

from textnode import TextNode, TextType
from markdown_processor import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node with different text", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_eq2(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)
    def test_noteq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    def test_noteq3(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a image node", TextType.IMAGE, "image.png")
        self.assertNotEqual(node, node2)


class TestSplitNodesDelimiterFunction(unittest.TestCase):
    def test_from_lesson(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        correct_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, correct_nodes)

    def test_from_lesson2(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        correct_nodes = [
            TextNode("This is text with a `code block` word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, correct_nodes)

    def test_from_lesson3(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "_", TextType.ITALIC)
        correct_nodes = [
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, correct_nodes)

    def test_from_lesson4(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        correct_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, correct_nodes)


class TestExtractFunctions(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(  
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)" 
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_no_images(self):
        matches = extract_markdown_images(  
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)" 
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_image_empty(self):
        matches = extract_markdown_images(  
            "This is text with an ![]()" 
        )
        self.assertListEqual([("", "")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(  
            "This is text with a link to [python logo](https://i.imgur.com/zjjcJKZ.png)" 
        )
        self.assertListEqual([("python logo", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_no_links(self):
        matches = extract_markdown_links(  
            "This is text with a ![python logo](https://i.imgur.com/zjjcJKZ.png)" 
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_link_empty(self):
        matches = extract_markdown_links(  
            "This is text with a link to []()" 
        )
        self.assertListEqual([("", "")], matches)



class TestSplitNodesOnImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images2(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images3(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                )
            ],
            new_nodes,
        )

    def test_split_images4(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)with stuff on the end.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("with stuff on the end.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and a [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links2(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and a ![second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ![second link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_links3(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)[second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links4(self):
        node = TextNode(
            "BEGINNING[link](https://i.imgur.com/zjjcJKZ.png)[second link](https://i.imgur.com/3elNhQu.png)END",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("BEGINNING", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("END", TextType.TEXT),
            ],
            new_nodes,
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_from_lesson(self):
        test_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        test_nodes = text_to_textnodes(test_text)
        correct_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(test_nodes, correct_nodes)

    def test2(self):
        test_text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)[link](https://boot.dev)Text at the end."
        test_nodes = text_to_textnodes(test_text)
        correct_nodes = [
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode("Text at the end.",TextType.TEXT)
        ]
        self.assertListEqual(test_nodes, correct_nodes)

    def test3(self):
        test_text = "[obi wan link](https://i.imgur.com/fJRm4Vk.jpeg)[link](https://boot.dev)Text at the end."
        test_nodes = text_to_textnodes(test_text)
        correct_nodes = [
            TextNode("obi wan link", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode("Text at the end.",TextType.TEXT)
        ]
        self.assertListEqual(test_nodes, correct_nodes)

    def test4(self):
        test_text = "BEGINNING[obi wan link](https://i.imgur.com/fJRm4Vk.jpeg)[link](https://boot.dev)END"
        test_nodes = text_to_textnodes(test_text)
        correct_nodes = [
            TextNode("BEGINNING",TextType.TEXT),
            TextNode("obi wan link", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode("END",TextType.TEXT)
        ]
        self.assertListEqual(test_nodes, correct_nodes)




if __name__ == "__main__":
    unittest.main()