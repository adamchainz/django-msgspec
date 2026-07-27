from __future__ import annotations

from collections.abc import Callable
from typing import Any

import msgspec.json
from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser as BaseJSONParser
from rest_framework.renderers import JSONRenderer as BaseJSONRenderer

from django_msgspec import enc_hook as django_msgspec_enc_hook


class JSONRenderer(BaseJSONRenderer):  # type: ignore[misc]
    enc_hook: Callable[[Any], Any] = staticmethod(django_msgspec_enc_hook)

    def render(
        self,
        data: Any,
        accepted_media_type: str | None = None,
        renderer_context: dict[str, Any] | None = None,
    ) -> bytes:
        if data is None:
            return b""

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        ret: bytes = msgspec.json.encode(data, enc_hook=self.enc_hook)
        if indent is not None:
            ret = msgspec.json.format(ret, indent=indent)
        return ret


class JSONParser(BaseJSONParser):  # type: ignore[misc]
    renderer_class = JSONRenderer

    def parse(
        self,
        stream: Any,
        media_type: str | None = None,
        parser_context: dict[str, Any] | None = None,
    ) -> Any:
        parser_context = parser_context or {}
        encoding = parser_context.get("encoding", settings.DEFAULT_CHARSET)
        data = stream.read()

        if isinstance(data, bytes) and encoding.lower().replace("_", "-") not in (
            "utf-8",
            "utf8",
        ):
            data = data.decode(encoding)

        try:
            return msgspec.json.decode(data)
        except ValueError as exc:
            raise ParseError(f"JSON parse error - {exc}") from exc
