Django REST framework
=====================

.. module:: django_msgspec.rest_framework

Extensions for using msgspec with |Django REST framework|__.

.. |Django REST framework| replace:: Django REST framework
__ https://www.django-rest-framework.org/

When using these, install django-msgspec with its ``drf`` extra to ensure Django REST framework compatibility, for example:

.. code-block:: console

    $ python -m pip install 'django-msgspec[drf]'

Then configure Django REST framework to swap the default JSON renderer and parser with the msgspec-based ones, for example:

.. code-block:: python

    REST_FRAMEWORK = {
        "DEFAULT_RENDERER_CLASSES": [
            "django_msgspec.rest_framework.JSONRenderer",
        ],
        "DEFAULT_PARSER_CLASSES": [
            "django_msgspec.rest_framework.JSONParser",
        ],
    }

.. autoclass:: JSONRenderer

   A subclass of |JSONRenderer|__ that serializes response data with ``msgspec.json.encode()``.

   .. |JSONRenderer| replace:: ``rest_framework.renderers.JSONRenderer``
   __ https://www.django-rest-framework.org/api-guide/renderers/#jsonrenderer

   The renderer uses msgspec’s native serialization path where possible, with :func:`django_msgspec.enc_hook` configured as msgspec’s ``enc_hook`` callable for extra Django type support such as lazy translation strings.

   Customize msgspec’s ``enc_hook`` parameter by subclassing:

   .. code-block:: python

       import pathlib

       from django_msgspec import enc_hook as base_enc_hook
       from django_msgspec.rest_framework import JSONRenderer


       class MyJSONRenderer(JSONRenderer):
           @staticmethod
           def enc_hook(obj):
               if isinstance(obj, pathlib.Path):
                   return str(obj)
               return base_enc_hook(obj)

.. autoclass:: JSONParser

   A subclass of |JSONParser|__ that parses request data with ``msgspec.json.decode()``.

   .. |JSONParser| replace:: ``rest_framework.parsers.JSONParser``
   __ https://www.django-rest-framework.org/api-guide/parsers/#jsonparser

Testing
-------

.. module:: django_msgspec.rest_framework.test

The following test case classes mirror |DRF’s test case classes|__, with django-msgspec’s :class:`APIClient` as ``client_class`` and django-msgspec’s JSON assertion methods:

.. |DRF’s test case classes| replace:: DRF’s test case classes
__ https://www.django-rest-framework.org/api-guide/testing/#api-test-cases

.. autoclass:: APISimpleTestCase

.. autoclass:: APITransactionTestCase

.. autoclass:: APITestCase

.. autoclass:: APILiveServerTestCase

Use them like DRF’s built-in classes:

.. code-block:: python

    from django_msgspec.rest_framework.test import APITestCase


    class MyAPITests(APITestCase):
        def test_create_account(self):
            response = self.client.post(
                "/accounts/",
                {"name": "DabApps"},
                format="json",
            )
            assert response.status_code == 201

.. autoclass:: APIClient

   A subclass of both :class:`django_msgspec.test.Client` and |APIClient|__.

   .. |APIClient| replace:: ``rest_framework.test.APIClient``
   __ https://www.django-rest-framework.org/api-guide/testing/#apiclient
