=========
Changelog
=========

1.0.1 (2026-08-07)
------------------

* Fix :func:`django_msgspec.enc_hook` to support Django’s ``SafeString``, as returned by Django’ss ``mark_safe()``.
  Previously, encoding a ``SafeString`` raised ``TypeError``.

1.0.0 (2026-07-28)
------------------

* Initial release.
