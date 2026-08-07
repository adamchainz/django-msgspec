from __future__ import annotations

from typing import Any

from django.utils.functional import Promise
from django.utils.safestring import SafeString


def enc_hook(obj: Any) -> Any:
    if isinstance(obj, Promise):
        return str(obj)
    if isinstance(obj, SafeString):
        # Convert to exact str (str() would return the SafeString unchanged).
        return obj[:]
    raise TypeError
