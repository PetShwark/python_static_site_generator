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
    