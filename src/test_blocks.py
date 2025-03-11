import unittest

from blocks import markdown_to_blocks


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


if __name__ == "__main__":
    _ = unittest.main()
