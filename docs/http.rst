HTTP responses
==============

.. currentmodule:: django_msgspec.http

.. autoclass:: JsonResponse

   A subclass of Django’s |HttpResponse|__ that serializes its content with |msgspec.json.encode()|__ instead of the standard library’s ``json.dumps()``.
   This provides faster serialization and native support for additional types such as ``datetime``, ``UUID``, and ``dataclasses``.

   .. |HttpResponse| replace:: ``HttpResponse``
   __ https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpResponse

   .. |msgspec.json.encode()| replace:: ``msgspec.json.encode()``
   __ https://msgspec.dev/api#msgspec.json.encode

   Usage mirrors Django’s built-in |JsonResponse|__:

   .. |JsonResponse| replace:: ``JsonResponse``
   __ https://docs.djangoproject.com/en/stable/ref/request-response/#jsonresponse-objects

   Unlike Django’s class, there is no ``safe`` parameter: any serializable object may be passed as ``data``, including non-\ ``dict`` objects like lists.
   Django deprecated ``safe`` in version 6.2 (`Ticket #36905 <https://code.djangoproject.com/ticket/36905>`__), as it guarded against a JSON hijacking vulnerability that only existed in long-obsolete browsers.

   .. code-block:: python

       from django_msgspec.http import JsonResponse


       def my_view(request):
           return JsonResponse({"key": "value"})

   :param data:
      The object to serialize.

   :param enc_hook:
      Passes through to |msgspec’s enc_hook parameter|__.
      Defaults to :func:`django_msgspec.enc_hook`, for extended type support.

      .. |msgspec’s enc_hook parameter| replace:: msgspec’s ``enc_hook`` parameter
      __ https://msgspec.dev/extending

      Pass a different callable to handle additional types, or chain to :func:`django_msgspec.enc_hook` for the built-in behaviour:

      .. code-block:: python

          import pathlib

          from django_msgspec import enc_hook as base_enc_hook


          def enc_hook(obj):
              if isinstance(obj, pathlib.Path):
                  return str(obj)
              return base_enc_hook(obj)


          JsonResponse({"path": pathlib.Path("/tmp/file.txt")}, enc_hook=enc_hook)

   :param kwargs:
      Other ``HttpResponse`` parameters.
