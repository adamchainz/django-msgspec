from __future__ import annotations

from collections.abc import Callable
from typing import Any

import msgspec.json
from django.utils.html import format_html
from django.utils.safestring import SafeString, mark_safe

from django_msgspec import enc_hook as _enc_hook

_json_script_escapes = {
    ord(">"): "\\u003E",
    ord("<"): "\\u003C",
    ord("&"): "\\u0026",
}


def json_script(
    value: Any,
    element_id: str | None = None,
    enc_hook: Callable[[Any], Any] = _enc_hook,
) -> SafeString:
    """
    Escape all the HTML/XML special characters with their unicode escapes, so
    value is safe to be output anywhere except for inside a tag attribute. Wrap
    the escaped JSON in a script tag.
    """
    json_str = (
        msgspec.json.encode(value, enc_hook=enc_hook)
        .decode()
        .translate(_json_script_escapes)
    )
    if element_id:
        template = '<script id="{}" type="application/json">{}</script>'
        args: tuple[Any, ...] = (element_id, mark_safe(json_str))
    else:
        template = '<script type="application/json">{}</script>'
        args = (mark_safe(json_str),)
    return format_html(template, *args)
