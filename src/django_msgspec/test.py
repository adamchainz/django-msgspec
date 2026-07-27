from __future__ import annotations

from typing import Any

import msgspec
import msgspec.json
from django.test import SimpleTestCase as DjangoSimpleTestCase
from django.test.client import JSON_CONTENT_TYPE_RE
from django.test.client import AsyncClient as DjangoAsyncClient
from django.test.client import Client as DjangoClient

from django_msgspec import enc_hook


class MsgspecMixin:
    def _encode_json(self, data: Any, content_type: str) -> Any:
        should_encode = JSON_CONTENT_TYPE_RE.match(content_type) and isinstance(
            data, (dict, list, tuple)
        )
        return msgspec.json.encode(data, enc_hook=enc_hook) if should_encode else data

    def _parse_json(self, response: Any, **extra: Any) -> Any:
        if extra:
            raise TypeError("msgspec.json.decode() does not accept keyword arguments")
        if not hasattr(response, "_json"):
            content_type = response.get("Content-Type")
            if not JSON_CONTENT_TYPE_RE.match(content_type):
                raise ValueError(
                    f'Content-Type header is "{content_type}", not "application/json"'
                )

            response._json = msgspec.json.decode(response.content)
        return response._json


class AsyncClient(MsgspecMixin, DjangoAsyncClient):
    pass


class Client(MsgspecMixin, DjangoClient):
    pass


class SimpleTestCase(DjangoSimpleTestCase):
    client_class = Client
    async_client_class = AsyncClient

    def assertJSONEqual(
        self, raw: str | bytes | bytearray, expected_data: Any, msg: str | None = None
    ) -> None:
        try:
            data = msgspec.json.decode(raw)
        except msgspec.DecodeError:
            self.fail(f"First argument is not valid JSON: {raw!r}")
        if isinstance(expected_data, (str, bytes, bytearray)):
            try:
                expected_data = msgspec.json.decode(expected_data)
            except msgspec.DecodeError:
                self.fail(f"Second argument is not valid JSON: {expected_data!r}")
        self.assertEqual(data, expected_data, msg=msg)

    def assertJSONNotEqual(
        self, raw: str | bytes | bytearray, expected_data: Any, msg: str | None = None
    ) -> None:
        try:
            data = msgspec.json.decode(raw)
        except msgspec.DecodeError:
            self.fail(f"First argument is not valid JSON: {raw!r}")
        if isinstance(expected_data, (str, bytes, bytearray)):
            try:
                expected_data = msgspec.json.decode(expected_data)
            except msgspec.DecodeError:
                self.fail(f"Second argument is not valid JSON: {expected_data!r}")
        self.assertNotEqual(data, expected_data, msg=msg)
