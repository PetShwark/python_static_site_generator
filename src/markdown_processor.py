from re import findall, search
from textnode import TextNode, TextType
from constants import MARKDOWN_IMAGE_RE, MARKDOWN_LINK_RE



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


def main():
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(f"Input: \n\t{text}")
    print(text_to_textnodes(text))

if __name__ == "__main__":
    main()