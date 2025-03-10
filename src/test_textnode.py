import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_when_no_url(self):
        node = TextNode("This is a url node", TextType.LINK)
        node2 = TextNode("This is a url node", TextType.LINK, "https://test.url")
        self.assertNotEqual(node, node2)

    def test_neq_empty_url(self):
        node = TextNode("This is a url node", TextType.LINK)
        node2 = TextNode("This is a url node", TextType.LINK, "")
        self.assertIsNone(node.url)
        self.assertNotEqual(node, node2)

    def test_url_is_none(self):
        node = TextNode("url node", TextType.LINK)
        self.assertIsNone(node.url)
        expected = "TextNode(url node, link, None)"
        self.assertEqual(expected, repr(node))

    def test_neq_text_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


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


if __name__ == "__main__":
    _ = unittest.main()
