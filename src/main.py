import os
from pathlib import Path
import sys

from markdown import extract_title, markdown_to_html_node


def generate_page(basepath: str, from_path: Path, template_path: Path, dest_path: Path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    try:
        with open(from_path, "r") as file:
            markdown = file.read()
        with open(template_path, "r") as file:
            template = file.read()

        content = markdown_to_html_node(markdown)
        title = extract_title(markdown)
        html_page = template.replace("{{ Title }}", title)
        html_page = html_page.replace("{{ Content }}", content.to_html())
        html_page = html_page.replace('href="/', f'href="{basepath}')
        html_page = html_page.replace('src="/', f'src="{basepath}')

        dest_path.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
        with open(dest_path, "w") as file:
            _ = file.write(html_page)

    except FileNotFoundError as e:
        print(f"'{e.filename}' not found")  # pyright: ignore[reportAny]
    except Exception as e:
        print(e)


def generate_pages_recursive(
    basepath: str, dir_path_content: Path, template_path: Path, dest_dir_path: Path
):
    entries: list[str] = os.listdir(dir_path_content)
    for entry in entries:
        entry_path = Path(os.path.join(dir_path_content, entry))
        new_dest_dir_path = Path(os.path.join(dest_dir_path, entry))

        if os.path.isfile(entry_path) and entry_path.suffix == ".md":
            generate_page(
                basepath,
                entry_path,
                template_path,
                new_dest_dir_path.with_suffix(".html"),
            )
        elif os.path.isdir(entry_path):
            generate_pages_recursive(
                basepath, entry_path, template_path, new_dest_dir_path
            )
        else:
            print(f"{entry}: unknown type of file")


def main(deploypath: str, basepath: str):
    from_path = Path("content")
    template_path = Path("template.html")
    dest_path = Path(deploypath)

    generate_pages_recursive(basepath, from_path, template_path, dest_path)


if __name__ == "__main__":
    deploypath = sys.argv[1] if len(sys.argv) >= 2 else "public"
    basepath = sys.argv[2] if len(sys.argv) >= 3 else "/"
    main(deploypath, basepath)
