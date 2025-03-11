import unittest

from blocks import BlockType, markdown_to_blocks, block_to_block_type


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


if __name__ == "__main__":
    _ = unittest.main()
