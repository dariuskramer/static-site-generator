from collections.abc import Sequence
from functools import reduce
from typing import override


class HTMLNode:
    tag: str
    value: str
    children: Sequence["HTMLNode"]
    props: dict[str, str]

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: Sequence["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag or ""
        self.value = value or ""
        self.children = children or []
        self.props = props or {}

    @override
    def __repr__(self):
        return f"""\
HTMLNode(tag={self.tag}, \
value="{self.value}", \
children={self.children}, \
props={self.props})"""

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        return reduce(lambda acc, p: acc + f' {p[0]}="{p[1]}"', self.props.items(), "")
