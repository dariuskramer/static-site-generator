from typing import Callable
from parentnode import ParentNode
from textnode import TextNode, TextType
from leafnode import LeafNode
from enum import Enum
import re

RE_IMAGE_PATTERN = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
RE_LINKS_PATTERN = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
RE_HEADING_PATTERN = r"^(#{1,6}) (.+)$"


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def textnode_to_htmlnode(text_node: TextNode) -> LeafNode:
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
                value=text_node.text,
                props={"src": text_node.url},
            )

    raise ValueError(f"No case matching for TextNode({text_node})!")  # pyright: ignore [reportUnreachable]


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


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]
    # CODE
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    # BOLD
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    # ITALIC
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    # IMAGE
    nodes = split_nodes_image(nodes)
    # LINK
    nodes = split_nodes_link(nodes)
    return nodes


def text_to_children(text: str) -> list[LeafNode]:
    textnodes: list[TextNode] = text_to_textnodes(text)
    children = [textnode_to_htmlnode(textnode) for textnode in textnodes]
    return children


def markdown_to_blocks(markdown: str) -> list[str]:
    return [line.strip() for line in markdown.split("\n\n") if line.strip()]


def block_to_block_type(text: str) -> BlockType:
    if not text:  # empty line
        return BlockType.PARAGRAPH

    if re.match(RE_HEADING_PATTERN, text):
        return BlockType.HEADING

    lines = text.splitlines()

    if len(lines) >= 2 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE

    starts_with_quote = [line for line in lines if line.startswith(">")]
    if len(lines) == len(starts_with_quote):
        return BlockType.QUOTE

    starts_with_dash = [line for line in lines if line.startswith("- ")]
    if len(lines) == len(starts_with_dash):
        return BlockType.UNORDERED_LIST

    valid_ordered_list = True
    for i, line in enumerate(lines, 1):
        if not line.startswith(f"{i}."):
            valid_ordered_list = False
            break
    if valid_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def block_to_html_code_node(block: str) -> ParentNode:
    lines = block.splitlines()
    value = "\n".join(lines[1:-1]) + "\n"
    return ParentNode("pre", [ParentNode("code", [LeafNode(None, value)])])


def block_to_html_heading_node(block: str) -> ParentNode:
    match = re.match(RE_HEADING_PATTERN, block)
    if not match:
        raise ValueError("Missing markdown heading!")

    level = match.group(1)
    value = match.group(2)
    children = text_to_children(value)
    return ParentNode(f"h{len(level)}", children)


def block_to_html_quote_node(block: str) -> ParentNode:
    # quote = "\n".join([line[2:] for line in block.splitlines()])
    quote = block.replace("> ", "").replace(">", "")
    children = block_to_html_paragraph_node(quote)
    return ParentNode("blockquote", [children])


def block_to_html_unordered_list_node(block: str) -> ParentNode:
    items = [line[2:] for line in block.splitlines()]
    children = [ParentNode("li", text_to_children(item)) for item in items]
    return ParentNode("ul", children)


def block_to_html_ordered_list_node(block: str) -> ParentNode:
    items = [line[3:] for line in block.splitlines()]
    children = [ParentNode("li", text_to_children(item)) for item in items]
    return ParentNode("ol", children)


def block_to_html_paragraph_node(block: str) -> ParentNode:
    paragraph = block.replace("\n", " ").strip()
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.CODE:
            return block_to_html_code_node(block)
        case BlockType.HEADING:
            return block_to_html_heading_node(block)
        case BlockType.QUOTE:
            return block_to_html_quote_node(block)
        case BlockType.UNORDERED_LIST:
            return block_to_html_unordered_list_node(block)
        case BlockType.ORDERED_LIST:
            return block_to_html_ordered_list_node(block)
        case BlockType.PARAGRAPH:
            return block_to_html_paragraph_node(block)

    raise ValueError(f"BlockType {BlockType} is unknown")  # pyright: ignore[reportUnreachable]


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    parents: list[ParentNode] = []

    for block in blocks:
        node = block_to_html_node(block)
        parents.append(node)

    return ParentNode("div", parents)
