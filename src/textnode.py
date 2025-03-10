from enum import Enum
from typing import override

from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    text: str
    text_type: TextType
    url: str | None

    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    @override
    def __eq__(self, textnode: object) -> bool:
        if not isinstance(textnode, TextNode):
            return NotImplemented
        return (
            self.text == textnode.text
            and self.text_type == textnode.text_type
            and self.url == textnode.url
        )

    @override
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: "TextNode"):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            if not text_node.url:
                raise Exception(
                    f"text_node.url is {text_node.url}: missing required url"
                )
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            if not text_node.url:
                raise Exception(
                    f"text_node.url is {text_node.url}: missing required url"
                )
            return LeafNode(
                tag="img",
                value="",
                props={"src": text_node.url, "alt": text_node.text},
            )
        case _:  # pyright: ignore [reportUnnecessaryComparison]
            raise Exception(f"No case matching for TextNode({text_node})!")  # pyright: ignore [reportUnreachable]
