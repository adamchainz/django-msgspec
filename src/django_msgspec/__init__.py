from __future__ import annotations

from typing import Any

from django.utils.functional import Promise


def enc_hook(obj: Any) -> Any:
    if isinstance(obj, Promise):
        return str(obj)
    raise TypeError
