=========
Changelog
=========

Unreleased
----------

* Switch package build backend from setuptools to `uv_build <https://docs.astral.sh/uv/concepts/build-backend/>`__.
  This makes builds with uv about nine times faster, since uv runs the backend natively, without creating a build environment or spawning a Python process.
  Additionally, source distributions no longer include test files, which setuptools previously included incompletely, missing the files needed to actually run them.

* Support Python 3.15.

1.0.1 (2026-08-07)
------------------

* Fix :func:`django_msgspec.enc_hook` to support Django’s ``SafeString``, as returned by Django’ss ``mark_safe()``.
  Previously, encoding a ``SafeString`` raised ``TypeError``.

1.0.0 (2026-07-28)
------------------

* Initial release.
