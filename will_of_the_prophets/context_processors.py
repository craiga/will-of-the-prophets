"""Context processors."""

from django.conf import settings


def sentry_dsn(request):  # noqa: ANN001, ANN201, ARG001, D103
    return {"sentry_dsn": settings.SENTRY_DSN}
