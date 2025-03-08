import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_parent_to_html_p(self):
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

    def test_initialization(self):
        children = [LeafNode(tag="p", value="Child paragraph")]
        node = ParentNode(tag="div", children=children, props={"class": "container"})

        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, {"class": "container"})
        self.assertIsNone(node.value)  # ParentNode should not have a value

    def test_to_html_with_valid_children(self):
        children = [
            LeafNode(tag="p", value="First paragraph"),
            LeafNode(tag="p", value="Second paragraph"),
        ]
        node = ParentNode(tag="div", children=children)
        expected_html = "<div><p>First paragraph</p><p>Second paragraph</p></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_props(self):
        children = [LeafNode(tag="p", value="Styled text")]
        node = ParentNode(tag="div", children=children, props={"class": "content"})
        expected_html = '<div class="content"><p>Styled text</p></div>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_without_tag_raises_error(self):
        children = [LeafNode(tag="p", value="No tag")]
        with self.assertRaises(ValueError):
            ParentNode(tag=None, children=children).to_html()

    def test_to_html_without_children_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode(tag="div", children=[]).to_html()

    def test_init_with_tag_and_children(self):
        children = [LeafNode("span", "child1"), LeafNode("span", "child2")]
        node = ParentNode("div", children)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, children)
        self.assertIsNone(node.props)

    def test_init_with_tag_children_and_props(self):
        children = [LeafNode("span", "child1"), LeafNode("span", "child2")]
        props = {"class": "container"}
        node = ParentNode("div", children, props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_to_html_with_children(self):
        children = [LeafNode("span", "child1"), LeafNode("span", "child2")]
        node = ParentNode("div", children)
        expected = "<div><span>child1</span><span>child2</span></div>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_children_and_props(self):
        children = [LeafNode("span", "child1"), LeafNode("span", "child2")]
        props = {"class": "container"}
        node = ParentNode("div", children, props)
        expected = '<div class="container"><span>child1</span><span>child2</span></div>'
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_nested_parent_nodes(self):
        inner_children = [LeafNode("span", "inner1"), LeafNode("span", "inner2")]
        inner_node = ParentNode("div", inner_children)
        outer_children = [LeafNode("p", "outer1"), inner_node]
        outer_node = ParentNode("section", outer_children)
        expected = "<section><p>outer1</p><div><span>inner1</span><span>inner2</span></div></section>"
        self.assertEqual(outer_node.to_html(), expected)

    def test_to_html_with_no_tag_raises_error(self):
        children = [LeafNode("span", "child1")]
        node = ParentNode(None, children)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "tag is required!")

    def test_to_html_with_no_children_raises_error(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "children is required!")

    def test_to_html_with_empty_children_raises_error(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "children is required!")

    if __name__ == "__main__":
        unittest.main()
