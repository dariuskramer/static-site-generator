import unittest

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
        expected = "TextNode(url node, link, None)"
        self.assertEqual(expected, node.__repr__())

    def test_neq_text_type(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    if __name__ == "__main__":
        unittest.main()
