def markdown_to_blocks(markdown: str) -> list[str]:
    return [line.strip() for line in markdown.split("\n\n") if line.strip()]
