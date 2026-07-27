from __future__ import annotations

from typing import Any

import msgspec.json

from django_msgspec import enc_hook as _enc_hook


class JSONSerializer:
    def dumps(self, obj: Any) -> bytes:
        value: bytes = msgspec.json.encode(obj, enc_hook=_enc_hook)
        return value

    def loads(self, data: bytes) -> Any:
        return msgspec.json.decode(data)
