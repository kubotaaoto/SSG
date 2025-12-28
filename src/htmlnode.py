class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        res = ""
        for key in self.props:  
            res += f' {key}="{self.props[key]}"'
        return res

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children={self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("invalid leaf node: no value")
        if not self.tag:
            return self.value
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("invalid parent node: no tag")
        if not self.children:
            raise ValueError(f"invalid parent node: no children in {self}")
        
        sub_res = ""
        for child in self.children:         
            sub_res += child.to_html()
        
        res = f"<{self.tag}{self.props_to_html()}>{sub_res}</{self.tag}>"
        return res

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

