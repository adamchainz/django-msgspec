from __future__ import annotations

from collections.abc import Callable
from typing import Any

import msgspec.json
from django.http import HttpResponse

from django_msgspec import enc_hook


class JsonResponse(HttpResponse):
    """
    An HTTP response class that consumes data to be serialized to JSON.

    :param data: Data to be dumped into json.
    :param enc_hook: A callable that gets called for objects that can’t
      otherwise be serialized. It should return a JSON encodable version of the
      object or raise a TypeError.
    """

    def __init__(
        self,
        data: Any,
        enc_hook: Callable[[Any], Any] = enc_hook,
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("content_type", "application/json")
        content = msgspec.json.encode(data, enc_hook=enc_hook)
        super().__init__(content=content, **kwargs)
