from __future__ import annotations

import datetime

import pytest
from django.test import SimpleTestCase
from rest_framework.test import APIClient as DRFAPIClient
from rest_framework.test import APILiveServerTestCase as DRFAPILiveServerTestCase
from rest_framework.test import APISimpleTestCase as DRFAPISimpleTestCase
from rest_framework.test import APITestCase as DRFAPITestCase
from rest_framework.test import APITransactionTestCase as DRFAPITransactionTestCase

from django_msgspec.http import JsonResponse
from django_msgspec.rest_framework.test import (
    APIClient,
    APILiveServerTestCase,
    APISimpleTestCase,
    APITestCase,
    APITransactionTestCase,
)
from django_msgspec.test import Client
from django_msgspec.test import SimpleTestCase as MsgspecSimpleTestCase


class APIClientTests(SimpleTestCase):
    def test_base_classes(self):
        assert issubclass(APIClient, Client)
        assert issubclass(APIClient, DRFAPIClient)

    def test_encode_data_explicit_json_content_type(self):
        data, content_type = APIClient()._encode_data(
            {"duration": datetime.timedelta(days=1, hours=2)},
            content_type="application/json",
        )

        assert data == b'{"duration":"P1DT7200S"}'
        assert content_type == "application/json"

    def test_parse_json(self):
        response = JsonResponse({"key": "value"})

        assert APIClient()._parse_json(response) == {"key": "value"}


@pytest.mark.parametrize(
    ("test_case_class", "drf_test_case_class"),
    [
        (APISimpleTestCase, DRFAPISimpleTestCase),
        (APITransactionTestCase, DRFAPITransactionTestCase),
        (APITestCase, DRFAPITestCase),
        (APILiveServerTestCase, DRFAPILiveServerTestCase),
    ],
)
def test_test_case_classes(test_case_class, drf_test_case_class):
    assert issubclass(test_case_class, MsgspecSimpleTestCase)
    assert issubclass(test_case_class, drf_test_case_class)
    assert test_case_class.client_class is APIClient


class APITestCaseTests(APITestCase):
    def test_client(self):
        assert self.client_class is APIClient
        assert isinstance(self.client, APIClient)
        assert isinstance(self.client, DRFAPIClient)

        data, content_type = self.client._encode_data(
            {"duration": datetime.timedelta(days=1, hours=2)},
            content_type="application/json",
        )
        assert data == b'{"duration":"P1DT7200S"}'
        assert content_type == "application/json"

    def test_assert_json_equal(self):
        self.assertJSONEqual(b'{"key":"value"}', {"key": "value"})
