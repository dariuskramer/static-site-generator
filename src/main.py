from pathlib import Path
from markdown import extract_title, markdown_to_html_node


def generate_page(from_path: Path, template_path: Path, dest_path: Path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    try:
        with open(from_path, "r") as file:
            markdown = file.read()
        with open(template_path, "r") as file:
            template = file.read()

        content = markdown_to_html_node(markdown)
        title = extract_title(markdown)
        html_page = template.replace("{{ Title }}", title).replace(
            "{{ Content }}", content.to_html()
        )

        with open(dest_path, "w") as file:
            _ = file.write(html_page)

    except FileNotFoundError as e:
        print(f"'{e.filename}' not found")  # pyright: ignore[reportAny]
    except Exception as e:
        print(f"Unknown error: {e}")


def main():
    from_path = Path("content/index.md")
    template_path = Path("template.html")
    dest_path = Path("public/index.html")

    generate_page(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()
