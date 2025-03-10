from textnode import TextNode, TextType
from leafnode import LeafNode


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


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
):
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        subtexts = node.text.split(delimiter)
        if len(subtexts) % 2 == 0:
            raise Exception(f"Invalid Markdown syntax: {node.text}")

        for i, subtext in enumerate(subtexts):
            # the first subtext is either an empty string (delimiter at the start)
            # or a text part not delimited
            if not subtext:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(subtext, node.text_type))
            else:
                new_nodes.append(TextNode(subtext, TextType(text_type)))

    return new_nodes
