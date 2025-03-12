import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "Alt text", {"src": "https://i.imgur.com/fJRm4Vk.jpeg"})
        self.assertEqual(
            node.to_html(),
            '<img alt="Alt text" src="https://i.imgur.com/fJRm4Vk.jpeg" />',
        )

    def test_initialization(self):
        node = LeafNode(tag="p", value="Hello, world!", props={"class": "text"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"class": "text"})

    def test_to_html_with_tag_and_value(self):
        node = LeafNode(tag="p", value="Hello, world!")
        expected_html = "<p>Hello, world!</p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_tag_value_and_props(self):
        node = LeafNode(
            tag="a",
            value="Click here",
            props={"href": "https://example.com", "target": "_blank"},
        )
        expected_html = '<a href="https://example.com" target="_blank">Click here</a>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_without_tag(self):
        node = LeafNode(tag=None, value="Just text")
        expected_html = "Just text"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_without_value_raises_error(self):
        with self.assertRaises(ValueError):
            _ = LeafNode(tag="p", value="").to_html()

    def test_to_html_with_empty_props(self):
        node = LeafNode(tag="span", value="Simple text", props={})
        expected_html = "<span>Simple text</span>"
        self.assertEqual(node.to_html(), expected_html)

    def test_init_with_tag_value_and_props(self):
        props = {"class": "bold", "id": "main"}
        node = LeafNode("p", "This is a paragraph", props)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph")
        self.assertEqual(node.props, props)

    def test_init_with_tag_and_value_only(self):
        node = LeafNode("a", "Click me")
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click me")
        self.assertIsNone(node.props)

    def test_to_html_with_tag_and_value_only(self):
        node = LeafNode("p", "This is a paragraph")
        expected = "<p>This is a paragraph</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_no_tag(self):
        node = LeafNode(None, "Raw text")
        expected = "Raw text"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_empty_value_raises_error(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError) as context:
            _ = node.to_html()
            self.assertEqual(str(context.exception), "all leaf must have a value!")

    def test_to_html_with_no_props(self):
        node = LeafNode("span", "Inline text")
        expected = "<span>Inline text</span>"
        self.assertEqual(node.to_html(), expected)


if __name__ == "__main__":
    _ = unittest.main()
