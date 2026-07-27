from __future__ import annotations

from typing import Any

import msgspec.json
from django.core.serializers.base import DeserializationError
from django.core.serializers.json import Deserializer as JSONDeserializer
from django.core.serializers.json import Serializer as JSONSerializer
from django.core.serializers.python import Deserializer as PythonDeserializer

from django_msgspec import enc_hook


class Serializer(JSONSerializer):
    _msgspec_indent: int | None

    def _init_options(self) -> None:
        super()._init_options()  # type: ignore [misc]
        self._msgspec_indent = self.options.get("indent") or None

    def end_object(self, obj: Any) -> None:
        if not self.first:
            self.stream.write(",")
            if not self._msgspec_indent:
                self.stream.write(" ")
        if self._msgspec_indent:
            self.stream.write("\n")
        dumped = msgspec.json.encode(self.get_dump_object(obj), enc_hook=enc_hook)
        if self._msgspec_indent:
            dumped = msgspec.json.format(dumped, indent=self._msgspec_indent)
        self.stream.write(dumped.decode())
        self._current = None


class Deserializer(JSONDeserializer):
    def __init__(self, stream_or_string: Any, **options: Any) -> None:
        if not isinstance(stream_or_string, (bytes, str)):
            stream_or_string = stream_or_string.read()
        try:
            objects = msgspec.json.decode(stream_or_string)
        except Exception as exc:
            raise DeserializationError(str(exc)) from exc
        PythonDeserializer.__init__(self, objects, **options)
