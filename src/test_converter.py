import unittest

from converter import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)
from leafnode import LeafNode
from textnode import TextNode, TextType


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_type_text(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        tested = text_node_to_html_node(text_node)
        expected = LeafNode(tag=None, value="Hello, world!")
        self.assertEqual(tested, expected)

    def test_text_type_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        expected = LeafNode(tag="b", value="Bold text")
        self.assertEqual(text_node_to_html_node(text_node), expected)

    def test_text_type_italic(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        expected = LeafNode(tag="i", value="Italic text")
        self.assertEqual(text_node_to_html_node(text_node), expected)

    def test_text_type_code(self):
        text_node = TextNode("Code snippet", TextType.CODE)
        expected = LeafNode(tag="code", value="Code snippet")
        self.assertEqual(text_node_to_html_node(text_node), expected)

    def test_text_type_link(self):
        text_node = TextNode("Click here", TextType.LINK, "https://example.com")
        expected = LeafNode(
            tag="a", value="Click here", props={"href": "https://example.com"}
        )
        self.assertEqual(text_node_to_html_node(text_node), expected)

    def test_text_type_image(self):
        text_node = TextNode(
            "An image", TextType.IMAGE, "https://example.com/image.png"
        )
        tested = text_node_to_html_node(text_node)
        expected = LeafNode(
            tag="img",
            value="",
            props={"src": "https://example.com/image.png", "alt": "An image"},
        )
        self.assertEqual(tested, expected)

    def test_invalid_text_type(self):
        # Create a TextNode with an invalid TextType (not part of the enum)
        class InvalidTextType:
            value: str = "value"

        text_node = TextNode("Invalid", InvalidTextType())  # pyright: ignore[reportArgumentType]
        with self.assertRaises(Exception) as context:
            _ = text_node_to_html_node(text_node)
        self.assertIn("No case matching for TextNode", str(context.exception))


class TestSplitNodesDelimiter(unittest.TestCase):
    # CODE BLOCK
    def test_single_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        textnode1, codenode, textnode2 = split_nodes_delimiter(
            [node], "`", TextType.CODE
        )
        self.assertEqual(textnode1, TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(codenode, TextNode("code block", TextType.CODE))
        self.assertEqual(textnode2, TextNode(" word", TextType.TEXT))

    def test_starts_with_code_block(self):
        node = TextNode("`code block` at the beginning", TextType.TEXT)
        codenode1, textnode = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(codenode1, TextNode("code block", TextType.CODE))
        self.assertEqual(textnode, TextNode(" at the beginning", TextType.TEXT))

    def test_ends_with_code_block(self):
        node = TextNode("code block at the end `code block`", TextType.TEXT)
        textnode, codenode2 = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(textnode, TextNode("code block at the end ", TextType.TEXT))
        self.assertEqual(codenode2, TextNode("code block", TextType.CODE))

    def test_only_one_code_block(self):
        node = TextNode("`code block`", TextType.TEXT)
        [codenode] = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(codenode, TextNode("code block", TextType.CODE))

    def test_only_one_empty_code_block(self):
        node = TextNode("``", TextType.TEXT)
        codenode = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(codenode, [])

    def test_starts_and_ends_with_code_block(self):
        node = TextNode(
            "`code block` at the beginning and the end `code block`", TextType.TEXT
        )
        codenode1, textnode, codenode2 = split_nodes_delimiter(
            [node], "`", TextType.CODE
        )
        self.assertEqual(codenode1, TextNode("code block", TextType.CODE))
        self.assertEqual(
            textnode, TextNode(" at the beginning and the end ", TextType.TEXT)
        )
        self.assertEqual(codenode2, TextNode("code block", TextType.CODE))

    def test_code_block_markdown_error(self):
        node = TextNode("markdown `error", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            _ = split_nodes_delimiter([node], "`", TextType.TEXT)
        self.assertIn("Invalid Markdown syntax", str(context.exception))

    def test_single_backquote_markdown_error(self):
        node = TextNode("`", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            _ = split_nodes_delimiter([node], "`", TextType.TEXT)
        self.assertIn("Invalid Markdown syntax", str(context.exception))

    def test_double_code_block_markdown_error(self):
        node = TextNode("markdown `error` markdown `", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            _ = split_nodes_delimiter([node], "`", TextType.TEXT)
        self.assertIn("Invalid Markdown syntax", str(context.exception))

    # BOLD
    def test_single_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        textnode1, boldnode, textnode2 = split_nodes_delimiter(
            [node], "**", TextType.BOLD
        )
        self.assertEqual(textnode1, TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(boldnode, TextNode("bold", TextType.BOLD))
        self.assertEqual(textnode2, TextNode(" word", TextType.TEXT))

    def test_starts_with_bold(self):
        node = TextNode("**bold** at the beginning", TextType.TEXT)
        boldnode, textnode = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(boldnode, TextNode("bold", TextType.BOLD))
        self.assertEqual(textnode, TextNode(" at the beginning", TextType.TEXT))

    def test_ends_with_bold(self):
        node = TextNode("bold at the end **bold**", TextType.TEXT)
        textnode, boldnode = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(textnode, TextNode("bold at the end ", TextType.TEXT))
        self.assertEqual(boldnode, TextNode("bold", TextType.BOLD))

    def test_only_one_bold(self):
        node = TextNode("**bold**", TextType.TEXT)
        [boldnode] = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(boldnode, TextNode("bold", TextType.BOLD))

    def test_only_one_empty_bold(self):
        node = TextNode("****", TextType.TEXT)
        boldnode = split_nodes_delimiter([node], "**", TextType.CODE)
        self.assertEqual(boldnode, [])

    def test_starts_and_ends_with_bold(self):
        node = TextNode("**bold** at the beginning and the end **bold**", TextType.TEXT)
        boldnode1, textnode, boldnode2 = split_nodes_delimiter(
            [node], "**", TextType.BOLD
        )
        self.assertEqual(boldnode1, TextNode("bold", TextType.BOLD))
        self.assertEqual(
            textnode, TextNode(" at the beginning and the end ", TextType.TEXT)
        )
        self.assertEqual(boldnode2, TextNode("bold", TextType.BOLD))

    def test_bold_markdown_error(self):
        node = TextNode("markdown **error", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            _ = split_nodes_delimiter([node], "**", TextType.TEXT)
        self.assertIn("Invalid Markdown syntax", str(context.exception))

    def test_single_bold_markdown_error(self):
        node = TextNode("**", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            _ = split_nodes_delimiter([node], "**", TextType.TEXT)
        self.assertIn("Invalid Markdown syntax", str(context.exception))

    def test_double_bold_markdown_error(self):
        node = TextNode("markdown **error** markdown **", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            _ = split_nodes_delimiter([node], "**", TextType.TEXT)
        self.assertIn("Invalid Markdown syntax", str(context.exception))

    # BOLD & ITALIC
    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )


class TestExtractMarkdownImages(unittest.TestCase):
    def test_two_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(result, expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_two_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(result, expected)


if __name__ == "__main__":
    _ = unittest.main()
