=========
Changelog
=========

Unreleased
----------

* Fix :func:`django_msgspec.enc_hook` to support Django’s ``SafeString``, as returned by Django’ss ``mark_safe()``.
  Previously, encoding a ``SafeString`` raised ``TypeError``.

1.0.0 (2026-07-28)
------------------

* Initial release.
