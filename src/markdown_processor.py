import os
from re import findall, search, MULTILINE, DOTALL
from enum import Enum
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from constants import MARKDOWN_IMAGE_RE, MARKDOWN_LINK_RE, MARKDOWN_HEADING_RE, MARKDOWN_CODEBLOCK_START_RE, MARKDOWN_CODEBLOCK_END_RE, MARKDOWN_QUOTE_RE, MARKDOWN_UL_RE, MARKDOWN_OL_RE


class BlockType(Enum):
    paragraph = "p"
    heading = "h"
    code = "code"
    quote = "blockquote"
    unordered_list = "ul"
    ordered_list = "ol"


def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list[TextNode]:
    """
    Split TextNodes in old_nodes by delimiter and assign text_type to the delimited parts.
    
    :param old_nodes: Nodes to split
    :type old_nodes: list[TextNode]
    :param delimiter: Delimiter string
    :type delimiter: str
    :param text_type: TextType to assign to delimited parts
    :type text_type: TextType
    :return: List of TextNodes with splits applied
    :rtype: list[TextNode]
    """
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            # There must be an even number of delimiters to split properly
            nodes_to_add: list[TextNode] = []
            delimited_parts = old_node.text.split(delimiter)
            if len(delimited_parts) % 2 == 0:
                raise Exception(f"Unmatched delimiter '{delimiter}' in text: {old_node.text}")
            for idx, part in enumerate(delimited_parts):
                if part:  # Only add non-empty parts
                    if idx % 2 == 0:
                        nodes_to_add.append(TextNode(part, TextType.TEXT))
                    else:
                        nodes_to_add.append(TextNode(part, text_type))
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
    if not md: return False
    return True if search(MARKDOWN_HEADING_RE, md) else False


def md_is_code(md:str) -> bool:
    if not md: return False
    md_lines = md.split("\n")
    code_start = search(MARKDOWN_CODEBLOCK_START_RE, md_lines[0]) # Check for beginning ticks on first line
    code_end = search(MARKDOWN_CODEBLOCK_END_RE, md_lines[-1]) # Check for ending ticks on last line
    return code_start and code_end


def md_is_quote(md:str) -> bool:
    if not md: return False
    md_lines = md.split("\n")
    result = True
    for md_line in md_lines:
        if not search(MARKDOWN_QUOTE_RE, md_line):
            result = False
            break
    return result


def md_is_ul(md:str) -> bool:
    if not md: return False
    md_lines = md.split("\n")
    result = True
    for md_line in md_lines:
        if not search(MARKDOWN_UL_RE, md_line):
            result = False
            break
    return result


def md_is_ol(md:str) -> bool:
    if not md: return False
    md_lines = md.split("\n")
    result = True
    for idx, md_line in enumerate(md_lines):
        a_match = search(MARKDOWN_OL_RE, md_line)
        if not a_match:
            result = False
            break
        else:
            if not int(a_match.group(1)) == idx+1:
                result = False
                break
    return result



def block_to_block_type(md:str) -> BlockType:
    if md_is_heading(md): return BlockType.heading
    elif md_is_code(md): return BlockType.code
    elif md_is_quote(md): return BlockType.quote
    elif md_is_ul(md): return BlockType.unordered_list
    elif md_is_ol(md): return BlockType.ordered_list
    else: return BlockType.paragraph


def heading_block_to_parent_node(md:str) -> ParentNode:
    heading_match = search(MARKDOWN_HEADING_RE, md)
    if heading_match: # should always be true here because of block type check
        heading_level = len(heading_match.group(1)) # (#{1,6}) in regex
        heading_text = heading_match.group(2).strip() # (.*) in regex
        text_nodes = text_to_textnodes(heading_text)
        html_children = [text_node_to_html_node(tn) for tn in text_nodes if tn.text.strip()]
        return ParentNode(f'h{heading_level}', html_children)
    else:
        raise Exception("Invalid heading block")
    

def paragraph_block_to_parent_node(md:str) -> ParentNode:
    md = md.replace("\n", " ")
    text_nodes = text_to_textnodes(md)
    html_children = [text_node_to_html_node(tn) for tn in text_nodes if tn.text.strip()]
    return ParentNode('p', html_children)


def quote_block_to_parent_node(md:str) -> ParentNode:
    # Remove leading "> " from each line
    quote_lines = md.split("\n")
    cleaned_lines = []
    for line in quote_lines:
        quote_match = search(MARKDOWN_QUOTE_RE, line)
        if quote_match:
            cleaned_lines.append(quote_match.group(2).strip())
    quote_text = "\n".join(cleaned_lines)
    text_nodes = text_to_textnodes(quote_text)
    html_children = [text_node_to_html_node(tn) for tn in text_nodes if tn.text.strip()]
    return ParentNode('blockquote', html_children)


def unordered_list_block_to_parent_node(md:str) -> ParentNode:
    # Remove leading "- " from each line
    ul_lines = md.split("\n")
    li_nodes = []
    for line in ul_lines:
        ul_match = search(MARKDOWN_UL_RE, line)
        if ul_match:
            li_text = ul_match.group(2).strip()
            text_nodes = text_to_textnodes(li_text)
            html_children = [text_node_to_html_node(tn) for tn in text_nodes if tn.text.strip()]
            li_nodes.append(ParentNode('li', html_children))
    return ParentNode('ul', li_nodes)


def ordered_list_block_to_parent_node(md:str) -> ParentNode:
    # Remove leading "#. " from each line
    ol_lines = md.split("\n")
    li_nodes = []
    for line in ol_lines:
        ol_match = search(MARKDOWN_OL_RE, line)
        if ol_match:
            li_text = ol_match.group(2).strip()
            text_nodes = text_to_textnodes(li_text)
            html_children = [text_node_to_html_node(tn) for tn in text_nodes if tn.text.strip()]
            li_nodes.append(ParentNode('li', html_children))
    return ParentNode('ol', li_nodes)


def code_block_to_parent_node(md:str) -> ParentNode:
    code_content = md.split("\n")[1:-1]  # Remove the starting and ending ``` lines
    code_node = TextNode("\n".join(code_content)+"\n", TextType.CODE)
    html_children = [text_node_to_html_node(code_node)]
    return ParentNode('pre', html_children)


def markdown_to_html_node(markdown:str) -> ParentNode:
    text_blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in text_blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.heading:
                html_nodes.append(heading_block_to_parent_node(block))
            case BlockType.code:
                html_nodes.append(code_block_to_parent_node(block))
            case BlockType.quote:
                html_nodes.append(quote_block_to_parent_node(block))
            case BlockType.unordered_list:
                html_nodes.append(unordered_list_block_to_parent_node(block))
            case BlockType.ordered_list:
                html_nodes.append(ordered_list_block_to_parent_node(block))
            case BlockType.paragraph:
                html_nodes.append(paragraph_block_to_parent_node(block))
    return ParentNode("div", html_nodes)


def extract_title(markdown:str) -> str:
    text_blocks = markdown_to_blocks(markdown)
    for block in text_blocks:
        if md_is_heading(block):
            heading_match = search(MARKDOWN_HEADING_RE, block)
            if heading_match and len(heading_match.group(1)) == 1:  # Only consider level 1 headings as title
                return heading_match.group(2).strip()
    raise Exception("No level 1 heading found for title")


def generate_page(basepath: str, from_path: str, template_path: str, dest_path: str):
    """
    Generate a full HTML page from a markdown file and a template.

    :param basepath: Base path for the site
    :type basepath: str
    :param from_path: Markdown file path
    :type from_path: str
    :param template_path: Template file path
    :type template_path: str
    :param dest_path: Destination HTML file path
    :type dest_path: str
    """
    print(f"Generating page from markdown file, {from_path}, using template, {template_path}, to {dest_path}")
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    title = extract_title(markdown_content)

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    full_html = template_content.replace("{{ Content }}", html_content).replace("{{ Title }}", title).replace("href=\"/",f"href=\"{basepath}").replace("src=\"/",f"src=\"{basepath}")

    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(full_html)


def generate_pages_recursively(basepath: str, from_dir: str, template_path: str, dest_dir: str):
    """
    Recursively generate HTML pages from markdown files in a directory using a template.
    
    :param basepath: Base path for the site
    :type basepath: str
    :param from_dir: Source directory containing markdown files
    :type from_dir: str
    :param template_path: Template file path
    :type template_path: str
    :param dest_dir: Destination directory for generated HTML files
    :type dest_dir: str
    """
    for root, dirs, files in os.walk(from_dir):
        for file in files:
            if file.endswith('.md'):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, from_dir)
                dest_path = os.path.join(dest_dir, os.path.splitext(relative_path)[0] + '.html')
                generate_page(basepath,from_path, template_path, dest_path)


def main():
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
    print(f"md: {md}")
    node = markdown_to_html_node(md)
    html = node.to_html()
    print(f"html: {html}")
    print(f"len html: {len(html)}")

if __name__ == "__main__":
    main()