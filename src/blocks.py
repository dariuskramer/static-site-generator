import re
from enum import Enum

RE_HEADING_PATTERN = r"^#{1,6} .+"
RE_CODE_BLOCK_PATTERN = r"^```$"


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


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
