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
            raise NotImplementedError
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

        props = super().props_to_html()
        if self.tag == "img":
            if not self.props or "src" not in self.props:
                raise ValueError("'src' attribute is required!")

            return f'<{self.tag} alt="{self.value}" {props} />'

        if props:
            return f"<{self.tag} {props}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
