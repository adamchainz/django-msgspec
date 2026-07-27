from __future__ import annotations

from typing import Any

from django import template
from django.utils.safestring import SafeString

from django_msgspec.html import json_script as _json_script

register = template.Library()


@register.filter(is_safe=True)
def json_script(value: Any, element_id: str | None = None) -> SafeString:
    """
    Output value JSON-encoded with msgspec, wrapped in a
    <script type="application/json"> tag (with an optional id).
    """
    return _json_script(value, element_id)
