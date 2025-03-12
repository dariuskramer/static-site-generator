import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            'class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(tag="div", value="Test", children=None, props={"class": "test"})
        expected_repr = (
            "HTMLNode(tag=div, value=\"Test\", children=None, props={'class': 'test'})"
        )
        self.assertEqual(repr(node), expected_repr)

    def test_repr2(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=p, value=\"What a strange world\", children=None, props={'class': 'primary'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

    def test_initialization_with_default_values(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_initialization_with_values(self):
        children = [HTMLNode(tag="div", value="Hello", children=None, props=None)]
        props = {"class": "container", "id": "main"}

        node = HTMLNode(tag="span", value="Test", children=children, props=props)

        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "Test")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_props_to_html(self):
        node = HTMLNode(
            tag="div", value="Test", children=[], props={"class": "test", "id": "main"}
        )
        props_html = node.props_to_html()
        expected_props_html = 'class="test" id="main"'
        self.assertEqual(props_html, expected_props_html)

    def test_props_to_html_empty_props(self):
        node = HTMLNode(tag="div", value="Test", children=[])
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
        expected_props_html = 'class="btn" disabled="true"'
        self.assertEqual(props_html, expected_props_html)

    def test_init_with_all_properties(self):
        children = [HTMLNode()]
        props = {"class": "bold"}
        node = HTMLNode("div", "Hello", children, props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_repr_with_children_and_props(self):
        node = HTMLNode("a", "link", [HTMLNode()], {"href": "https://example.com"})
        expected = "HTMLNode(tag=a, value=\"link\", children=[HTMLNode(tag=None, value=\"None\", children=None, props=None)], props={'href': 'https://example.com'})"
        self.assertEqual(repr(node), expected)

    def test_props_to_html_with_empty_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_single_prop(self):
        node = HTMLNode(props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), 'href="https://example.com"')

    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        props_html = node.props_to_html()
        self.assertIn('href="https://example.com"', props_html)
        self.assertIn('target="_blank"', props_html)

    def test_to_html_raises_not_implemented_error(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            _ = node.to_html()


if __name__ == "__main__":
    _ = unittest.main()
