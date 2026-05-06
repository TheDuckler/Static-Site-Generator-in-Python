

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        formatted_string = ""
        if self.props == None or self.props == {}:
            return formatted_string
        else:
            for attributes in self.props:
                formatted_string += f" {attributes}='{self.props[attributes]}'"

        return formatted_string
    
    def __eq__(self, other):
        if (self.tag == other.tag) and (self.value == other.value) and (self.children == other.children) and (self.props == other.props):
            return True

    def __repr__(self):
        return f"tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props}"
    

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNodes must have a value")
        if self.tag == None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"tag = {self.tag}, value = {self.value}, props = {self.props}"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNodes must have a tag")
        if self.children == None or self.children == []:
            raise ValueError("ParentNodes must have children")
        
        return f"<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"
    
