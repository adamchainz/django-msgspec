from __future__ import annotations

import decimal
from typing import Any

import msgspec.json
from django.test import SimpleTestCase

from django_msgspec.http import JsonResponse


class JsonResponseTests(SimpleTestCase):
    def test_basic(self):
        response = JsonResponse({"key": "value"})
        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"
        assert msgspec.json.decode(response.content) == {"key": "value"}

    def test_content_type_custom(self):
        response = JsonResponse({}, content_type="application/json; charset=utf-8")
        assert response["Content-Type"] == "application/json; charset=utf-8"

    def test_list(self):
        response = JsonResponse([1, 2, 3])
        assert msgspec.json.decode(response.content) == [1, 2, 3]

    def test_enc_hook(self):
        def enc_hook(obj: Any) -> Any:
            if isinstance(obj, decimal.Decimal):
                return str(obj)
            raise TypeError  # pragma: no cover

        response = JsonResponse({"value": decimal.Decimal("1.5")}, enc_hook=enc_hook)
        assert msgspec.json.decode(response.content) == {"value": "1.5"}

    def test_status_code(self):
        response = JsonResponse({}, status=201)
        assert response.status_code == 201
