import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_initialization_with_default_values(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_initialization_with_values(self):
        children = [HTMLNode(tag="div", value="Hello")]
        props = {"class": "container", "id": "main"}

        node = HTMLNode(tag="span", value="Test", children=children, props=props)

        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "Test")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_repr(self):
        node = HTMLNode(tag="div", value="Test", children=[], props={"class": "test"})
        expected_repr = (
            "HTMLNode(tag=div, value=\"Test\", children=[], props={'class': 'test'})"
        )
        self.assertEqual(repr(node), expected_repr)

    def test_props_to_html(self):
        node = HTMLNode(
            tag="div", value="Test", children=[], props={"class": "test", "id": "main"}
        )
        props_html = node.props_to_html()
        expected_props_html = ' class="test" id="main"'
        self.assertEqual(props_html, expected_props_html)

    def test_props_to_html_empty_props(self):
        node = HTMLNode(tag="div", value="Test", children=[], props={})
        props_html = node.props_to_html()
        self.assertEqual(props_html, "")

    def test_props_to_html_with_multiple_properties(self):
        node = HTMLNode(
            tag="button",
            value="Click me",
            children=[],
            props={"class": "btn", "disabled": "true"},
        )
        props_html = node.props_to_html()
        expected_props_html = ' class="btn" disabled="true"'
        self.assertEqual(props_html, expected_props_html)

    def test_init_with_all_properties(self):
        children = [HTMLNode()]
        props = {"class": "bold"}
        node = HTMLNode("div", "Hello", children, props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_init_with_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr_with_children_and_props(self):
        node = HTMLNode("a", "link", [HTMLNode()], {"href": "https://example.com"})
        expected = "HTMLNode(tag=a, value=\"link\", children=[HTMLNode(tag=None, value=\"None\", children=None, props=None)], props={'href': 'https://example.com'})"
        self.assertEqual(repr(node), expected)

    def test_props_to_html_with_empty_props(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_single_prop(self):
        node = HTMLNode(props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        props_html = node.props_to_html()
        self.assertIn('href="https://example.com"', props_html)
        self.assertIn('target="_blank"', props_html)

    def test_to_html_raises_not_implemented_error(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    if __name__ == "__main__":
        unittest.main()
