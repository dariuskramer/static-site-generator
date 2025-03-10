from textnode import TextNode, TextType
from htmlnode import HTMLNode


def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    props = {
        "href": "https://www.boot.dev",
        "target": "_blank",
    }
    node = HTMLNode("a", "link to Boot.dev", None, props)
    print(node.props_to_html())
    print(node)


if __name__ == "__main__":
    main()
