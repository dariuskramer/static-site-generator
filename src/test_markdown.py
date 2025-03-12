import unittest

from leafnode import LeafNode
from markdown import (
    BlockType,
    block_to_block_type,
    block_to_html_code_node,
    block_to_html_heading_node,
    block_to_html_ordered_list_node,
    block_to_html_paragraph_node,
    block_to_html_quote_node,
    block_to_html_unordered_list_node,
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
    markdown_to_blocks,
    markdown_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    textnode_to_htmlnode,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_type_text(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        tested = textnode_to_htmlnode(text_node)
        expected = LeafNode(tag=None, value="Hello, world!")
        self.assertEqual(tested, expected)

    def test_text_type_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        expected = LeafNode(tag="b", value="Bold text")
        self.assertEqual(textnode_to_htmlnode(text_node), expected)

    def test_text_type_italic(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        expected = LeafNode(tag="i", value="Italic text")
        self.assertEqual(textnode_to_htmlnode(text_node), expected)

    def test_text_type_code(self):
        text_node = TextNode("Code snippet", TextType.CODE)
        expected = LeafNode(tag="code", value="Code snippet")
        self.assertEqual(textnode_to_htmlnode(text_node), expected)

    def test_text_type_link(self):
        text_node = TextNode("Click here", TextType.LINK, "https://example.com")
        expected = LeafNode(
            tag="a", value="Click here", props={"href": "https://example.com"}
        )
        self.assertEqual(textnode_to_htmlnode(text_node), expected)

    def test_text_type_image(self):
        text_node = TextNode(
            "An image", TextType.IMAGE, "https://example.com/image.png"
        )
        tested = textnode_to_htmlnode(text_node)
        expected = LeafNode(
            tag="img",
            value="An image",
            props={"src": "https://example.com/image.png"},
        )
        self.assertEqual(tested, expected)

    def test_invalid_text_type(self):
        # Create a TextNode with an invalid TextType (not part of the enum)
        class InvalidTextType:
            value: str = "value"

        text_node = TextNode("Invalid", InvalidTextType())  # pyright: ignore[reportArgumentType]
        with self.assertRaises(Exception) as context:
            _ = textnode_to_htmlnode(text_node)
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


class TestExtractTitle(unittest.TestCase):
    def test_title(self):
        text = """
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

## What's the deal?
Here's the deal, **I like Tolkien**.

## Quotes
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""
        result = extract_title(text)
        expected = "Tolkien Fan Club"
        self.assertEqual(result, expected)

    def test_missing_title(self):
        text = """
## Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

## What's the deal?
Here's the deal, **I like Tolkien**.

## Quotes
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""
        with self.assertRaises(Exception) as context:
            _ = extract_title(text)
        self.assertIn("h1 header missing", str(context.exception))


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_at_start_and_end(self):
        node = TextNode(
            "![start](https://i.imgur.com/zjjcJKZ.png) and another ![end](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_between_text(self):
        node = TextNode(
            "start with an ![image](https://i.imgur.com/zjjcJKZ.png) and end without one",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and end without one", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_only_one(self):
        node = TextNode(
            "![only one](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("only one", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_one_after_another(self):
        node = TextNode(
            "![first](https://i.imgur.com/zjjcJKZ.png)![second](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_at_start_and_end(self):
        node = TextNode(
            "[start](https://www.boot.dev) and [end](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("end", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_links_between_text(self):
        node = TextNode(
            "start with an [link](https://www.boot.dev) and end without one",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("start with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and end without one", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_only_one(self):
        node = TextNode(
            "[only one](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("only one", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_one_after_another(self):
        node = TextNode(
            "[first](https://www.boot.dev)[second](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "https://www.boot.dev"),
                TextNode(
                    "second", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )


class TestTextToTextnodes(unittest.TestCase):
    def test_from_bootdev(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_from_bootdev(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_basic_markdown(self):
        markdown = """
Ceci est un paragraphe.

Ceci est un autre paragraphe.
"""
        expected = ["Ceci est un paragraphe.", "Ceci est un autre paragraphe."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_lines(self):
        markdown = """


Ceci est un paragraphe.


Ceci est un autre paragraphe.


"""
        expected = ["Ceci est un paragraphe.", "Ceci est un autre paragraphe."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_leading_trailing_whitespace(self):
        markdown = """
    Ceci est un paragraphe.

\t
\t  Ceci est un autre paragraphe.  \t
"""
        expected = ["Ceci est un paragraphe.", "Ceci est un autre paragraphe."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_leading_trailing_whitespace_single_paragraph(self):
        markdown = """
    Ceci est un paragraphe.
\t
\t  Ceci est un autre paragraphe.  \t
"""
        expected = ["Ceci est un paragraphe.\n\t\n\t  Ceci est un autre paragraphe."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_blocks_with_whitespace(self):
        markdown = """   Premier bloc avec des espaces   

   Deuxième bloc avec des espaces   """
        expected = ["Premier bloc avec des espaces", "Deuxième bloc avec des espaces"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_single_paragraph(self):
        markdown = "Ceci est un seul paragraphe."
        expected = ["Ceci est un seul paragraphe."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_string(self):
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_no_double_newlines(self):
        markdown = "Ceci est une ligne\nCeci est une autre ligne"
        expected = ["Ceci est une ligne\nCeci est une autre ligne"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_mixed_content(self):
        markdown = """# Titre

- Une liste
- Avec des éléments

> Une citation"""
        expected = ["# Titre", "- Une liste\n- Avec des éléments", "> Une citation"]
        self.assertEqual(markdown_to_blocks(markdown), expected)


class TestBlockToBlockType(unittest.TestCase):
    def test_with_empty_line(self):
        markdown = ""
        result = block_to_block_type(markdown)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

    def test_heading_valid(self):
        markdown = "# heading 1"
        result = block_to_block_type(markdown)
        expected = BlockType.HEADING
        self.assertEqual(result, expected)

        markdown = "## heading 2"
        result = block_to_block_type(markdown)
        expected = BlockType.HEADING
        self.assertEqual(result, expected)

        markdown = "### heading 3"
        result = block_to_block_type(markdown)
        expected = BlockType.HEADING
        self.assertEqual(result, expected)

        markdown = "#### heading 4"
        result = block_to_block_type(markdown)
        expected = BlockType.HEADING
        self.assertEqual(result, expected)

        markdown = "##### heading 5"
        result = block_to_block_type(markdown)
        expected = BlockType.HEADING
        self.assertEqual(result, expected)

        markdown = "###### heading 6"
        result = block_to_block_type(markdown)
        expected = BlockType.HEADING
        self.assertEqual(result, expected)

    def test_heading_invalid(self):
        markdown = "####### heading 7"
        result = block_to_block_type(markdown)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

        markdown = "######## heading 8"
        result = block_to_block_type(markdown)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

    def test_code_block_empty(self):
        markdown = "```\n```"
        result = block_to_block_type(markdown)
        expected = BlockType.CODE
        self.assertEqual(result, expected)

    def test_code_block_single(self):
        markdown = "```\n"
        result = block_to_block_type(markdown)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

        markdown = "```"
        result = block_to_block_type(markdown)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

    def test_code_block_basic(self):
        markdown = """\
```
def example():
    print("Hello, World!")
```
"""
        result = block_to_block_type(markdown)
        expected = BlockType.CODE
        self.assertEqual(result, expected)

    def test_code_block_multilines(self):
        markdown = """\
```
def example():
    print("Hello, World!")

def example2():
    print("Hello, World!")
```
"""
        result = block_to_block_type(markdown)
        expected = BlockType.CODE
        self.assertEqual(result, expected)

    def test_quote_single_line(self):
        markdown = """\
> test
"""
        result = block_to_block_type(markdown)
        expected = BlockType.QUOTE
        self.assertEqual(result, expected)

    def test_quote_multilines(self):
        markdown = """\
> test
> test2
"""
        result = block_to_block_type(markdown)
        expected = BlockType.QUOTE
        self.assertEqual(result, expected)

    def test_quote_invalid_in_between(self):
        markdown = """\
> test
test2
> test3
"""
        result = block_to_block_type(markdown)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

    def test_quote_invalid_in_between_with_space(self):
        markdown = """\
> test
 > test2
> test3
"""
        result = block_to_block_type(markdown)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

    def test_unordered_list_single_line(self):
        markdown = """\
- test
"""
        result = block_to_block_type(markdown)
        expected = BlockType.UNORDERED_LIST
        self.assertEqual(result, expected)

    def test_unordered_list_multilines(self):
        markdown = """\
- test
- test2
"""
        result = block_to_block_type(markdown)
        expected = BlockType.UNORDERED_LIST
        self.assertEqual(result, expected)

    def test_unordered_list_invalid_in_between(self):
        markdown = """\
- test
test2
- test3
"""
        result = block_to_block_type(markdown)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

    def test_unordered_list_invalid_in_between_with_space(self):
        markdown = """\
- test
 - test2
- test3
"""
        result = block_to_block_type(markdown)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

    def test_ordered_list_block(self):
        markdown = """\
1. First item
2. Second item
3. Third item
"""
        result = block_to_block_type(markdown)
        expected = BlockType.ORDERED_LIST
        self.assertEqual(result, expected)

    def test_ordered_list_invalid(self):
        markdown = """\
1. First item
3. Second item
2. Third item
"""
        result = block_to_block_type(markdown)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

    def test_mixed_content_block(self):
        markdown = """\
- Item 1
> This is a quote.
1. First item
"""
        result = block_to_block_type(markdown)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

    def test_partial_code_block(self):
        markdown = """\
```
def example():
    print("Hello, World!")
"""
        result = block_to_block_type(markdown)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)


class TestBlockToHtmlHeadingNode(unittest.TestCase):
    def test_block_to_html_heading_node(self):
        result = block_to_html_heading_node("# Title level 1")
        expected = "<h1>Title level 1</h1>"
        self.assertEqual(result.to_html(), expected)

        result = block_to_html_heading_node("## Title level 2")
        expected = "<h2>Title level 2</h2>"
        self.assertEqual(result.to_html(), expected)

        result = block_to_html_heading_node("### Title level 3")
        expected = "<h3>Title level 3</h3>"
        self.assertEqual(result.to_html(), expected)

        result = block_to_html_heading_node("#### Title level 4")
        expected = "<h4>Title level 4</h4>"
        self.assertEqual(result.to_html(), expected)

        result = block_to_html_heading_node("##### Title level 5")
        expected = "<h5>Title level 5</h5>"
        self.assertEqual(result.to_html(), expected)

        result = block_to_html_heading_node("###### Title level 6")
        expected = "<h6>Title level 6</h6>"
        self.assertEqual(result.to_html(), expected)

    def test_block_to_html_heading_node_with_bold(self):
        result = block_to_html_heading_node("# Title level 1 with **bold**")
        expected = "<h1>Title level 1 with <b>bold</b></h1>"
        self.assertEqual(result.to_html(), expected)

    def test_block_to_html_heading_node_with_italic(self):
        result = block_to_html_heading_node("# Title level 1 with _italic_")
        expected = "<h1>Title level 1 with <i>italic</i></h1>"
        self.assertEqual(result.to_html(), expected)

    def test_block_to_html_heading_node_with_code(self):
        result = block_to_html_heading_node("# Title level 1 with `code`")
        expected = "<h1>Title level 1 with <code>code</code></h1>"
        self.assertEqual(result.to_html(), expected)

    def test_block_to_html_heading_node_with_link(self):
        result = block_to_html_heading_node(
            "# Title level 1 with a [link](https://boot.dev)"
        )
        expected = '<h1>Title level 1 with a <a href="https://boot.dev">link</a></h1>'
        self.assertEqual(result.to_html(), expected)


class TestBlockToHtmlCodeNode(unittest.TestCase):
    def test_block_to_html_code_node(self):
        markdown = """\
```
def hello():
    print("hello")

def world():
    print("world")
```
"""
        result = block_to_html_code_node(markdown)
        expected = '<pre><code>def hello():\n    print("hello")\n\ndef world():\n    print("world")\n</code></pre>'
        self.assertEqual(result.to_html(), expected)

    def test_block_to_html_code_node_dont_inline(self):
        markdown = """\
```
This is a line with a **bold** word
This is a line with an _italic_ word
This is a line with a `code` word
This is a line with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)
This is a line with a [link](https://boot.dev) at the end
```
"""
        result = block_to_html_code_node(markdown)
        expected = """<pre><code>\
This is a line with a **bold** word
This is a line with an _italic_ word
This is a line with a `code` word
This is a line with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)
This is a line with a [link](https://boot.dev) at the end
</code></pre>\
"""
        self.assertEqual(result.to_html(), expected)


class TestBlockToHtmlQuoteNode(unittest.TestCase):
    def test_block_to_html_quote_node_single_line(self):
        markdown = """\
> This is a quote
"""
        result = block_to_html_quote_node(markdown)
        expected = "<blockquote>This is a quote</blockquote>"
        self.assertEqual(result.to_html(), expected)

    def test_block_to_html_quote_node_multi_lines(self):
        markdown = """\
> This is a
> multilines
> quote
"""
        result = block_to_html_quote_node(markdown)
        expected = "<blockquote>This is a multilines quote</blockquote>"
        self.assertEqual(result.to_html(), expected)

    @unittest.skip("what behavior do I want?")
    def test_block_to_html_quote_node_empty_line(self):
        markdown = """\
> This is a quote with an empty line in between
>
> This is a quote with an empty line in between
"""
        result = block_to_html_quote_node(markdown)
        expected = "<blockquote>This is a quote with an empty line in between\nThis is a quote with an empty line in between</blockquote>"
        self.assertEqual(result.to_html(), expected)

    def test_block_to_html_quote_node_with_inline(self):
        markdown = """\
> This is a line with a **bold** word
> This is a line with an _italic_ word
> This is a line with a `code` word
> This is a line with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)
> This is a line with a [link](https://boot.dev) at the end
"""
        result = block_to_html_quote_node(markdown)
        expected = """\
<blockquote>\
This is a line with a <b>bold</b> word \
This is a line with an <i>italic</i> word \
This is a line with a <code>code</code> word \
This is a line with an <img alt="obi wan image" src="https://i.imgur.com/fJRm4Vk.jpeg" /> \
This is a line with a <a href="https://boot.dev">link</a> at the end\
</blockquote>\
"""
        self.maxDiff = None  # pyright: ignore[reportUnannotatedClassAttribute]
        self.assertEqual(result.to_html(), expected)


class TestBlockToHtmlUnorderedListNode(unittest.TestCase):
    def test_block_to_html_unordered_list(self):
        markdown = """\
- item 1
- item 2
- item 3
"""
        result = block_to_html_unordered_list_node(markdown)
        expected = "<ul><li>item 1</li><li>item 2</li><li>item 3</li></ul>"
        self.assertEqual(result.to_html(), expected)

    def test_block_to_html_unordered_list_only_one(self):
        markdown = """\
- item
"""
        result = block_to_html_unordered_list_node(markdown)
        expected = "<ul><li>item</li></ul>"
        self.assertEqual(result.to_html(), expected)

    def test_block_to_html_unordered_list_node_with_inline(self):
        markdown = """\
- This is a line with a **bold** word
- This is a line with an _italic_ word
- This is a line with a `code` word
- This is a line with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)
- This is a line with a [link](https://boot.dev) at the end
"""
        result = block_to_html_unordered_list_node(markdown)
        expected = """\
<ul>\
<li>This is a line with a <b>bold</b> word</li>\
<li>This is a line with an <i>italic</i> word</li>\
<li>This is a line with a <code>code</code> word</li>\
<li>This is a line with an <img alt="obi wan image" src="https://i.imgur.com/fJRm4Vk.jpeg" /></li>\
<li>This is a line with a <a href="https://boot.dev">link</a> at the end</li>\
</ul>\
"""
        self.maxDiff = None  # pyright: ignore[reportUnannotatedClassAttribute]
        self.assertEqual(result.to_html(), expected)


class TestBlockToHtmlOrderedListNode(unittest.TestCase):
    def test_block_to_html_ordered_list(self):
        markdown = """\
1. item 1
2. item 2
3. item 3
"""
        result = block_to_html_ordered_list_node(markdown)
        expected = "<ol><li>item 1</li><li>item 2</li><li>item 3</li></ol>"
        self.assertEqual(result.to_html(), expected)

    def test_block_to_html_ordered_list_only_one(self):
        markdown = """\
1. item
"""
        result = block_to_html_ordered_list_node(markdown)
        expected = "<ol><li>item</li></ol>"
        self.assertEqual(result.to_html(), expected)

    def test_block_to_html_ordered_list_node_with_inline(self):
        markdown = """\
1. This is a line with a **bold** word
2. This is a line with an _italic_ word
3. This is a line with a `code` word
4. This is a line with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)
5. This is a line with a [link](https://boot.dev) at the end
"""
        result = block_to_html_ordered_list_node(markdown)
        expected = """\
<ol>\
<li>This is a line with a <b>bold</b> word</li>\
<li>This is a line with an <i>italic</i> word</li>\
<li>This is a line with a <code>code</code> word</li>\
<li>This is a line with an <img alt="obi wan image" src="https://i.imgur.com/fJRm4Vk.jpeg" /></li>\
<li>This is a line with a <a href="https://boot.dev">link</a> at the end</li>\
</ol>\
"""
        self.maxDiff = None  # pyright: ignore[reportUnannotatedClassAttribute]
        self.assertEqual(result.to_html(), expected)


class TestBlockToHtmlParagraphNode(unittest.TestCase):
    def test_block_to_html_paragraph_single_line(self):
        markdown = """\
single line
"""
        result = block_to_html_paragraph_node(markdown)
        expected = "<p>single line</p>"
        self.assertEqual(result.to_html(), expected)

    def test_block_to_html_paragraph_multi_line(self):
        markdown = """\
multilines
paragraph
hello world and good morning!
"""
        result = block_to_html_paragraph_node(markdown)
        expected = "<p>multilines paragraph hello world and good morning!</p>"
        self.assertEqual(result.to_html(), expected)

    def test_block_to_html_paragraph_with_inline_markdown(self):
        markdown = """\
This is a line with a **bold** word
This is a line with an _italic_ word
This is a line with a `code` word
This is a line with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)
This is a line with a [link](https://boot.dev) at the end
"""
        result = block_to_html_paragraph_node(markdown)
        expected = "<p>"
        expected += "This is a line with a <b>bold</b> word"
        expected += " This is a line with an <i>italic</i> word"
        expected += " This is a line with a <code>code</code> word"
        expected += ' This is a line with an <img alt="obi wan image" src="https://i.imgur.com/fJRm4Vk.jpeg" />'
        expected += (
            ' This is a line with a <a href="https://boot.dev">link</a> at the end'
        )
        expected += "</p>"
        self.maxDiff = None  # pyright: ignore[reportUnannotatedClassAttribute]
        self.assertEqual(result.to_html(), expected)


class TestMarkdownToHtmlBlocks(unittest.TestCase):
    def test_bootdev_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_bootdev_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    _ = unittest.main()
