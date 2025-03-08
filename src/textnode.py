from enum import Enum


class TextType(Enum):
    NORMAL_TEXT = "normal"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "itali"
    CODE_TEXT = "code"
    LINK_TEXT = "link"
    IMAGE_TEXT = "image"


class TextNode:
    def __init__(self, text: str, text_type: str, url: str = None):
        self.text, self.text_type, self.url = text, TextType(text_type), url

    def __eq__(self, textnode: "TextNode"):
        return (
            self.text == textnode.text
            and self.text_type == textnode.text_type
            and self.url == textnode.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
