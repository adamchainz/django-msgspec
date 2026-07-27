from __future__ import annotations

import datetime
import decimal
from io import BytesIO
from zoneinfo import ZoneInfo

import msgspec.json
import pytest
from django.test import SimpleTestCase
from rest_framework.exceptions import ParseError

from django_msgspec.rest_framework import JSONParser, JSONRenderer


class JSONRendererTests(SimpleTestCase):
    def test_basic(self):
        result = JSONRenderer().render({"key": "value"})
        assert result == b'{"key":"value"}'
        assert msgspec.json.decode(result) == {"key": "value"}

    def test_none(self):
        assert JSONRenderer().render(None) == b""

    def test_indent_from_media_type(self):
        result = JSONRenderer().render(
            {"key": ["value"]}, accepted_media_type="application/json; indent=4"
        )
        assert result == b'{\n    "key": [\n        "value"\n    ]\n}'

    def test_indent_from_context(self):
        result = JSONRenderer().render({"key": "value"}, renderer_context={"indent": 2})
        assert result == b'{\n  "key": "value"\n}'

    def test_datetime_utc_native(self):
        result = JSONRenderer().render(
            {"value": datetime.datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC"))}
        )
        assert msgspec.json.decode(result) == {"value": "2024-01-01T00:00:00Z"}

    def test_custom_enc_hook(self):
        class Thing:
            pass

        def thing_enc_hook(obj):
            if isinstance(obj, Thing):
                return "thing"
            raise TypeError  # pragma: no cover

        class ThingJSONRenderer(JSONRenderer):
            enc_hook = staticmethod(thing_enc_hook)

        result = ThingJSONRenderer().render({"value": Thing()})
        assert msgspec.json.decode(result) == {"value": "thing"}

    def test_decimal(self):
        result = JSONRenderer().render({"value": decimal.Decimal("1.5")})
        assert msgspec.json.decode(result) == {"value": "1.5"}

    def test_timedelta(self):
        result = JSONRenderer().render({"value": datetime.timedelta(seconds=1)})
        assert msgspec.json.decode(result) == {"value": "PT1S"}


class JSONParserTests(SimpleTestCase):
    def test_basic(self):
        result = JSONParser().parse(BytesIO(b'{"key":"value"}'))
        assert result == {"key": "value"}

    def test_non_utf8_encoding(self):
        data = '{"key":"£"}'.encode("utf-16")
        result = JSONParser().parse(
            BytesIO(data), parser_context={"encoding": "utf-16"}
        )
        assert result == {"key": "£"}

    def test_invalid_json_raises_parse_error(self):
        with pytest.raises(ParseError, match="JSON parse error"):
            JSONParser().parse(BytesIO(b"not valid json"))
