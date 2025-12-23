from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag:str|None=None, value:str|None=None, children:list[HTMLNode]|None=None, props:dict|None=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self) -> str:
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def props_to_html(self) -> str:
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return f'<{self.tag} {self.props_to_html()}>{self.value}{"".join(str(child) for child in self.children)}</{self.tag}>'  
    

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("Value cannot be empty for LeafNode")
        if not self.tag:
            return self.value
        props_html = self.props_to_html()
        return f'<{self.tag}{" " + props_html if props_html else ""}>{self.value}</{self.tag}>'
    

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict = None):
        super().__init__(tag, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Tag cannot be empty for ParentNode")
        if not self.children:
            raise ValueError("Children cannot be empty for ParentNode")
        props_html = self.props_to_html()
        children_html = "".join(child.to_html() for child in self.children)
        return f'<{self.tag}{" " + props_html if props_html else ""}>{children_html}</{self.tag}>'

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unsupported TextType: {text_node.text_type}")