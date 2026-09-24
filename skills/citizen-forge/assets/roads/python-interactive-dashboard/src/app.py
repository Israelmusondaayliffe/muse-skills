from html import escape
from typing import Iterable


def render(rows: Iterable[str]) -> str:
    items = "".join("<li>{}</li>".format(escape(str(row))) for row in rows)
    return "<!doctype html><html><body><h1>Dashboard</h1><ul>{}</ul></body></html>".format(items)
