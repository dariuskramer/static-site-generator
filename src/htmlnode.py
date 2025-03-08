from functools import reduce


class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: ["HTMLNode"] = [],
        props: dict = {},
    ):
        self.tag, self.value, self.children, self.props = tag, value, children, props

    def __repr__(self):
        return f"""\
HTMLNode(tag={self.tag}, \
value="{self.value}", \
children={self.children}, \
props={self.props})"""

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return reduce(lambda acc, p: acc + f' {p[0]}="{p[1]}"', self.props.items(), "")
