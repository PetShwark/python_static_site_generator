import unittest

from markdown_processor import markdown_to_blocks, markdown_to_html_node, BlockType, block_to_block_type


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
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

    def test_markdown_to_blocks2(self):
        md = """
This is **bolded** paragraph.        Here's a lot of space between a sentence.

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph.        Here's a lot of space between a sentence.",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_to_blocks3(self):
        md = """
This is **bolded** paragraph.        Here's a lot of space between a sentence.

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

 - This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph.        Here's a lot of space between a sentence.",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestMarkdownToBlocks(unittest.TestCase):
    def test1(self):
        input_string = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

```Code Block
Mode code```

> This is a quote.
> - Mark Twain

- This is the first list item in a list block
- This is a list item
- This is another list item

1. This is the first list item in a list block
2. This is a list item
3. This is another list item
4. This is another list item
"""
        blocks = markdown_to_blocks(input_string)
        self.assertEqual(block_to_block_type(blocks[0]),BlockType.heading) 
        self.assertEqual(block_to_block_type(blocks[1]),BlockType.paragraph)
        self.assertEqual(block_to_block_type(blocks[2]),BlockType.code)
        self.assertEqual(block_to_block_type(blocks[3]),BlockType.quote)
        self.assertEqual(block_to_block_type(blocks[4]),BlockType.unordered_list)
        self.assertEqual(block_to_block_type(blocks[5]),BlockType.ordered_list) 



    def test2(self):
        input_string = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

``Code Block
Mode code```

> This is a quote.
 - Mark Twain

- This is the first list item in a list block
-This is a list item
- This is another list item

1. This is the first list item in a list block
1. This is a list item
3. This is another list item
4. This is another list item
"""
        blocks = markdown_to_blocks(input_string)
        self.assertEqual(block_to_block_type(blocks[0]),BlockType.heading) 
        self.assertEqual(block_to_block_type(blocks[1]),BlockType.paragraph)
        self.assertEqual(block_to_block_type(blocks[2]),BlockType.paragraph)
        self.assertEqual(block_to_block_type(blocks[3]),BlockType.paragraph)
        self.assertEqual(block_to_block_type(blocks[4]),BlockType.paragraph)
        self.assertEqual(block_to_block_type(blocks[5]),BlockType.paragraph) 



    def test3(self):
        input_string = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

``Code Block
Mode code```

> This is a quote.
 - Mark Twain

- This is the first list item in a list block
-This is a list item
- This is another list item

0. This is the first list item in a list block
1. This is a list item
2. This is another list item
3. This is another list item
"""
        blocks = markdown_to_blocks(input_string)
        self.assertEqual(block_to_block_type(blocks[0]),BlockType.heading) 
        self.assertEqual(block_to_block_type(blocks[1]),BlockType.paragraph)
        self.assertEqual(block_to_block_type(blocks[2]),BlockType.paragraph)
        self.assertEqual(block_to_block_type(blocks[3]),BlockType.paragraph)
        self.assertEqual(block_to_block_type(blocks[4]),BlockType.paragraph)
        self.assertEqual(block_to_block_type(blocks[5]),BlockType.paragraph) 


class TestMarkdownToParentNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """This is **bolded** paragraph
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

    def test_heading_and_lists(self):
        md = """
# Heading

- List item
- Another list item
- Third list item

1. First ordered item
2. Second ordered item
3. Third ordered item
4. Fourth ordered item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><ul><li>List item</li><li>Another list item</li><li>Third list item</li></ul><ol><li>First ordered item</li><li>Second ordered item</li><li>Third ordered item</li><li>Fourth ordered item</li></ol></div>",
        )

    def test_quote(self):
        md = """> This is a quote.
> - Mark Twain
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote.\n- Mark Twain</blockquote></div>",
        )