from re import findall, search, MULTILINE, DOTALL
from enum import Enum
from textnode import TextNode, TextType
from constants import MARKDOWN_IMAGE_RE, MARKDOWN_LINK_RE, MARKDOWN_HEADING_RE, MARKDOWN_CODEBLOCK_START_RE, MARKDOWN_CODEBLOCK_END_RE


class BlockType(Enum):
    paragraph = "p"
    heading = "h"
    code = "code"
    quote = "blockquote"
    unordered_list = "ul"
    ordered_list = "ol"


def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            nodes_to_add: list[TextNode] = []
            delimited_parts = old_node.text.split(delimiter, 2)
            if len(delimited_parts) == 2: # only one delimiter - bad syntax
                raise Exception(f"Bad Markdown syntax - only one delimiter ({delimiter}) found.")
            if len(delimited_parts) == 1: # no delimiter - treat as text
                nodes_to_add.append(old_node)
            else: # must be split into 3 
                nodes_to_add.append(TextNode(delimited_parts[0], TextType.TEXT))
                nodes_to_add.append(TextNode(delimited_parts[1], text_type))
                nodes_to_add.append(TextNode(delimited_parts[2], TextType.TEXT))
            new_nodes.extend(nodes_to_add)
    return new_nodes


def extract_markdown_images(text:str) -> list:
    return findall(MARKDOWN_IMAGE_RE, text)

        
def extract_markdown_links(text:str) -> list:
    return findall(MARKDOWN_LINK_RE, text)


def split_nodes_image(old_nodes):
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            nodes_to_add: list[TextNode] = []
            extract_from_text = old_node.text
            search_start_idx = 0
            while True:
                a_match = search(MARKDOWN_IMAGE_RE, extract_from_text)
                if a_match:
                    match_start_idx = a_match.start()
                    match_end_idx = a_match.end()
                    if match_start_idx != search_start_idx:
                        nodes_to_add.append(TextNode(extract_from_text[search_start_idx:match_start_idx], TextType.TEXT))
                    nodes_to_add.append(TextNode(a_match.group(1),TextType.IMAGE,a_match.group(2)))
                    extract_from_text = extract_from_text[match_end_idx:]
                else:
                    break
            if extract_from_text:
                nodes_to_add.append(TextNode(extract_from_text, TextType.TEXT))
            if nodes_to_add:
                new_nodes.extend(nodes_to_add)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            nodes_to_add: list[TextNode] = []
            extract_from_text = old_node.text
            search_start_idx = 0
            while True:
                a_match = search(MARKDOWN_LINK_RE, extract_from_text)
                if a_match:
                    match_start_idx = a_match.start()
                    match_end_idx = a_match.end()
                    if match_start_idx != search_start_idx:
                        nodes_to_add.append(TextNode(extract_from_text[search_start_idx:match_start_idx], TextType.TEXT))
                    nodes_to_add.append(TextNode(a_match.group(1),TextType.LINK,a_match.group(2)))
                    extract_from_text = extract_from_text[match_end_idx:]
                else:
                    break
            if extract_from_text:
                nodes_to_add.append(TextNode(extract_from_text, TextType.TEXT))
            if nodes_to_add:
                new_nodes.extend(nodes_to_add)
    return new_nodes


def text_to_textnodes(text:str) -> list[TextNode]:
    initial_list = [TextNode(text,TextType.TEXT)]
    list_with_images = split_nodes_image(initial_list)
    list_with_links = split_nodes_link(list_with_images)
    list_with_bold = split_nodes_delimiter(list_with_links, "**", TextType.BOLD)
    list_with_italic = split_nodes_delimiter(list_with_bold, "_", TextType.ITALIC)
    list_with_code = split_nodes_delimiter(list_with_italic, "`", TextType.CODE)
    return list_with_code


def markdown_to_blocks(text:str) -> list[str]:
    blocks = text.split("\n\n")
    return [x.strip() for x in blocks if x]


def md_is_heading(md:str) -> bool:
    return True if search(MARKDOWN_HEADING_RE, md) else False


def md_is_code(md:str) -> bool:
    if not md: return False
    md_lines = md.split("\n")
    code_start = search(MARKDOWN_CODEBLOCK_START_RE, md_lines[0])
    code_end = search(MARKDOWN_CODEBLOCK_END_RE, md_lines[-1])
    return code_start and code_end


def md_is_quote(md:str) -> bool:
    return False


def md_is_ul(md:str) -> bool:
    return False


def md_is_ol(md:str) -> bool:
    return False


def block_to_block_type(md:str) -> BlockType:
    if md_is_heading(md): return BlockType.heading
    elif md_is_code(md): return BlockType.code
    elif md_is_quote(md): return BlockType.quote
    elif md_is_ul(md): return BlockType.unordered_list
    elif md_is_ol(md): return BlockType.ordered_list
    else: return BlockType.paragraph


def main():
    input_string = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

```Code Block
Mode code```

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
    blocks = markdown_to_blocks(input_string)
    print(blocks)
    for block in blocks:
        print(f"{block}\n\tis a(n) {block_to_block_type(block)}")

if __name__ == "__main__":
    main()