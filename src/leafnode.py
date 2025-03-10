from typing import override
from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    """A LeafNode is a type of HTMLNode that represents a single HTML tag with no children."""

    def __init__(
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ):
        super().__init__(tag, value, props=props)

    @override
    def __eq__(self, other: object):
        if not isinstance(other, HTMLNode):
            return NotImplemented
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    @override
    def to_html(self) -> str:
        if not self.value:
            raise ValueError("all leaf must have a value!")
        if not self.tag:
            return self.value
        props = ""
        if self.props:
            props = super().props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
