from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag:str|None=None, value:str|None=None, children:list|None=None, props:dict|None=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self) -> str:
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def props_to_html(self) -> str:
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        if self.tag is None:
            return self.value if self.value is not None else ""
        props_html = self.props_to_html()
        return f'<{self.tag}{" " + props_html if props_html else ""}>value="{self.value if self.value is not None else ""}"{"".join(str(child) for child in self.children)}</{self.tag}>'  
    

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError(f"Value cannot be empty for LeafNode: tag={self.tag}, value={self.value}, props={self.props}")
        if not self.tag:
            return self.value
        if self.tag == "img":
            props_html = self.props_to_html()
            return f'<{self.tag}{" " + props_html if props_html else ""} />'
        props_html = self.props_to_html()
        return f'<{self.tag}{" " + props_html if props_html else ""}>{self.value}</{self.tag}>'
    

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError(f"Tag cannot be empty for ParentNode, tag={self.tag}, children={self.children}, props={self.props}")
        if not self.children:
            raise ValueError(f"Children cannot be empty for ParentNode, tag={self.tag}, children={self.children}, props={self.props}")
        props_html = self.props_to_html()
        children_html = "".join(child.to_html() for child in self.children)
        return f'<{self.tag}{" " + props_html if props_html else ""}>{children_html}</{self.tag}>'
    

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
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
            return LeafNode("img", text_node.text, props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unsupported TextType: {text_node.text_type}")