from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    """A LeafNode is a type of HTMLNode that represents a single HTML tag with no children."""

    def __init__(self, tag: str, value: str, props: dict = {}):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("all leaf must have a value!")
        if not self.tag:
            return self.value
        props = ""
        if self.props:
            props = super().props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
