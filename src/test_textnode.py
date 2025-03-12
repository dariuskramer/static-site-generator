import unittest

from markdown import textnode_to_htmlnode
from textnode import TextNode, TextType


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
        expected = 'TextNode("url node", link, None)'
        self.assertEqual(expected, repr(node))

    def test_neq_text_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    _ = unittest.main()
