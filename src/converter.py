from typing import Callable
from textnode import TextNode, TextType
from leafnode import LeafNode
import re

RE_IMAGE_PATTERN = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
RE_LINKS_PATTERN = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"


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
) -> list[TextNode]:
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


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(RE_IMAGE_PATTERN, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(RE_LINKS_PATTERN, text)


def _split_nodes_func(
    old_nodes: list[TextNode],
    pattern: str,
    extract_func: Callable[[str], list[tuple[str, str]]],
    text_type: TextType,
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = re.finditer(pattern, node.text)
        items: list[tuple[str, str]] = extract_func(node.text)
        start_string = 0
        for match, item in zip(matches, items):
            start_match, end_match = match.span()
            alt_txt, url = item
            subtext = node.text[start_string:start_match]
            if subtext:  # don't add empty string
                new_nodes.append(TextNode(subtext, node.text_type))
            new_nodes.append(TextNode(alt_txt, text_type, url))

            start_string = end_match

        if start_string < len(node.text):  # text remaining at the end
            new_nodes.append(TextNode(node.text[start_string:], node.text_type))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_func(
        old_nodes, RE_IMAGE_PATTERN, extract_markdown_images, TextType.IMAGE
    )


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_func(
        old_nodes, RE_LINKS_PATTERN, extract_markdown_links, TextType.LINK
    )
