enc_hook function
=================

.. currentmodule:: django_msgspec

.. function:: enc_hook(obj)

   A function for use with |msgspec’s enc_hook parameter|__ that extends msgspec to support serializing these extra types:

   .. |msgspec’s enc_hook parameter| replace:: msgspec’s ``enc_hook`` parameter
   __ https://msgspec.dev/extending

   * Django’s ``Promise`` objects, as used for `lazy translations <https://docs.djangoproject.com/en/stable/topics/i18n/translation/#lazy-translations>`__.

   * Django’s ``SafeString`` objects, as returned by |mark_safe()|__, which msgspec does not encode natively since it’s a ``str`` subclass.

   .. |mark_safe()| replace:: ``mark_safe()``
   __ https://docs.djangoproject.com/en/stable/ref/utils/#django.utils.safestring.mark_safe

   msgspec natively supports every other type that Django’s ``DjangoJSONEncoder`` handles: ``decimal.Decimal``, ``uuid.UUID``, and all ``datetime`` types including ``timedelta``.
   Two behavioural differences from ``DjangoJSONEncoder``:

   * ``timedelta`` values are encoded in msgspec’s compact ISO 8601 form, e.g. ``"P1DT7200S"`` rather than ``"P1DT02H00M00S"``.
     Django’s ``parse_duration()`` accepts both forms.
   * Timezone-aware ``datetime.time`` values are encoded with their offset, e.g. ``"12:30:00Z"``, where ``DjangoJSONEncoder`` raises ``ValueError``.

   This function is analogous to Django’s |DjangoJSONEncoder|__, which extends the standard library ``json`` module support to extra types.
   You won’t typically need to use this function directly, as it is used internally by the other utilities in this package.

   .. |DjangoJSONEncoder| replace:: ``DjangoJSONEncoder``
   __ https://docs.djangoproject.com/en/stable/topics/serialization/#djangojsonencoder
