from collections.abc import Sequence
from functools import reduce
from typing import override

from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    """
    Handle the nesting of HTML nodes inside of one another.
    Any HTML node that's not "leaf" node (i.e. it has children) is a "parent" node.
    """

    def __init__(
        self,
        tag: str,
        children: Sequence[HTMLNode],
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag=tag, value="", children=children, props=props)

    @override
    def to_html(self):
        if not self.tag:
            raise ValueError("tag is required!")
        if not self.children:
            raise ValueError("children is required!")
        props = ""
        if self.props:
            props = super().props_to_html()
        # children_to_html = "".join([child.to_html() for child in self.children])
        children_to_html = reduce(lambda acc, c: acc + c.to_html(), self.children, "")
        return f"<{self.tag}{props}>{children_to_html}</{self.tag}>"
