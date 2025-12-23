from textnode import TextNode, TextType

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

        
def main():
    node = TextNode("This is text with a code block word.", TextType.TEXT)
    node2 = TextNode("This is text with an _italic_ word.", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    print(f"Input: {node}")
    print(new_nodes)

if __name__ == "__main__":
    main()