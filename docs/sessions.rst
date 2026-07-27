Sessions
========

.. module:: django_msgspec.sessions

.. autoclass:: JSONSerializer

   A msgspec-based session serializer, replacing Django's built-in |JSONSerializer|__.

   .. |JSONSerializer| replace:: ``JSONSerializer``
   __ https://docs.djangoproject.com/en/stable/topics/http/sessions/#session-serialization

   Configure it in your settings:

   .. code-block:: python

       SESSION_SERIALIZER = "django_msgspec.sessions.JSONSerializer"

   .. warning:: **One-way migration**

      Migrating from Django’s ``JSONSerializer`` to django-msgspec’s is safe, but the reverse case is not.

      Sessions written by Django’s ``JSONSerializer`` can be read by django-msgspec’s without issue.
      But sessions written by django-msgspec’s ``JSONSerializer`` can be silently misread by Django’s.

      See the note in :doc:`signing` for more information—Django’s session ``JSONSerializer`` is a re-export of the signing one, so they share this limitation.
