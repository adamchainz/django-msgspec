from __future__ import annotations

import django.core.signing as signing
import pytest
from django.core.signing import JSONSerializer as DjangoJSONSerializer
from django.test import TestCase

from django_msgspec.signing import JSONSerializer


class JSONSerializerDirectTests(TestCase):
    def test_dumps_returns_bytes(self):
        result = JSONSerializer().dumps({"key": "value"})
        assert isinstance(result, bytes)

    def test_roundtrip_dict(self):
        data = {"key": "value", "num": 42, "list": [1, 2, 3]}
        s = JSONSerializer()
        assert s.loads(s.dumps(data)) == data

    def test_roundtrip_nested(self):
        data = {"nested": {"a": 1, "b": [True, False, None]}}
        s = JSONSerializer()
        assert s.loads(s.dumps(data)) == data

    def test_roundtrip_list(self):
        data = [1, "two", 3.0, None]
        s = JSONSerializer()
        assert s.loads(s.dumps(data)) == data


class SigningDumpsLoadsTests(TestCase):
    def test_roundtrip(self):
        data = {"user_id": 1, "action": "confirm"}
        token = signing.dumps(data, serializer=JSONSerializer)
        assert signing.loads(token, serializer=JSONSerializer) == data

    def test_roundtrip_list(self):
        data = [1, 2, 3]
        token = signing.dumps(data, serializer=JSONSerializer)
        assert signing.loads(token, serializer=JSONSerializer) == data

    def test_token_is_string(self):
        token = signing.dumps({"x": 1}, serializer=JSONSerializer)
        assert isinstance(token, str)

    def test_tampered_token_raises(self):
        token = signing.dumps({"x": 1}, serializer=JSONSerializer)

        with pytest.raises(signing.BadSignature):
            signing.loads(token + "x", serializer=JSONSerializer)


class TimestampSignerTests(TestCase):
    def test_sign_unsign_object(self):
        signer = signing.TimestampSigner()
        data = {"key": "value", "num": 42}
        signed = signer.sign_object(data, serializer=JSONSerializer)
        assert signer.unsign_object(signed, serializer=JSONSerializer) == data

    def test_max_age_not_expired(self):
        signer = signing.TimestampSigner()
        data = {"action": "verify"}
        signed = signer.sign_object(data, serializer=JSONSerializer)
        result = signer.unsign_object(signed, serializer=JSONSerializer, max_age=60)
        assert result == data


class JSONSerializerCompatibilityTests(TestCase):
    """
    Migrating from Django's JSONSerializer to django-msgspec's is safe, but
    the reverse case is not. Django's JSONSerializer.loads decodes payloads
    as latin-1 before parsing, so tokens signed with django-msgspec's
    JSONSerializer (raw UTF-8) round-trip silently to mojibake rather than
    raising.
    """

    def test_django_json_signed_loaded_by_msgspec(self):
        data = {"user_id": 1, "action": "confirm"}
        token = signing.dumps(data, serializer=DjangoJSONSerializer)
        assert signing.loads(token, serializer=JSONSerializer) == data

    def test_msgspec_signed_loaded_by_django_json(self):
        data = {"user_id": 1, "action": "confirm"}
        token = signing.dumps(data, serializer=JSONSerializer)
        assert signing.loads(token, serializer=DjangoJSONSerializer) == data

    def test_django_json_signed_loaded_by_msgspec_non_ascii(self):
        data = {"username": "héllo", "city": "東京"}
        token = signing.dumps(data, serializer=DjangoJSONSerializer)
        assert signing.loads(token, serializer=JSONSerializer) == data

    @pytest.mark.xfail
    def test_msgspec_signed_loaded_by_django_json_non_ascii(self):
        """
        Tokens signed with django-msgspec's JSONSerializer are silently
        corrupted when loaded by Django's JSONSerializer, which decodes the
        payload as latin-1 before parsing.
        """
        data = {"username": "héllo", "city": "東京"}
        token = signing.dumps(data, serializer=JSONSerializer)
        loaded = signing.loads(token, serializer=DjangoJSONSerializer)
        assert loaded == data, (
            f"Token signed by django-msgspec's JSONSerializer was loaded by Django's"
            f" JSONSerializer as {loaded!r}, silently corrupting non-ASCII"
            f" strings via latin-1 decode of UTF-8 bytes."
        )
