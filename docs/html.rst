HTML utilities
==============

.. currentmodule:: django_msgspec.html

.. autofunction:: json_script

   A msgspec-powered version of Django’s |json_script|__ utility.
   It serializes ``value`` with ``msgspec.json.encode()``, escapes HTML/XML special characters, and wraps the result in a ``<script type="application/json">`` tag.

   .. |json_script| replace:: ``json_script()``
   __ https://docs.djangoproject.com/en/stable/ref/utils/#django.utils.html.json_script

   .. code-block:: python

       from django_msgspec.html import json_script

       json_script({"key": "value"}, "data")

   :param value:
      The object to serialize.

   :param element_id:
      An optional ``id`` attribute for the ``<script>`` tag.

   :param enc_hook:
      Passes through to msgspec; defaults to :func:`django_msgspec.enc_hook`.

``json_script`` template filter
-------------------------------

A template filter equivalent to Django’s built-in |json_script_filter|__, using the function above.
In your templates:

.. |json_script_filter| replace:: ``json_script``
__ https://docs.djangoproject.com/en/stable/ref/templates/builtins/#json-script

.. code-block:: html+django

    {% load django_msgspec %}
    {{ data|json_script:"my-data" }}
