"""Fixtures used across tests."""

import logging
import os
import re
from datetime import datetime
from unittest import mock
from urllib.parse import urlparse, urlunparse

from django.conf import settings
from django.http import QueryDict
from django.test.utils import override_settings

import pytest
import pytz
from model_bakery import baker

logger = logging.getLogger(__name__)


@pytest.fixture
def rolls():
    """Generate nine rolls on the first nine days of July 2369."""
    for number in range(1, 10):
        embargo = pytz.utc.localize(
            datetime(year=2369, month=7, day=number, hour=12, minute=34, second=56)
        )
        baker.make("Roll", number=number, embargo=embargo)


@pytest.fixture(scope="session", autouse=True)
def _set_settings():
    """Global settings for all tests."""
    with override_settings(
        AWS_S3_REGION_NAME="us-east-1",
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "TIMEOUT": 0,
            }
        },
        DEBUG=False,
        PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
        SECURE_SSL_REDIRECT=True,
        WHITENOISE_AUTOREFRESH=True,
        STATICFILES_STORAGE="whitenoise.storage.CompressedStaticFilesStorage",
    ):
        yield


@pytest.fixture(scope="session", autouse=True)
def _set_environment_variables():
    """Override global environment variables in all tests."""
    with mock.patch.dict(
        os.environ,
        {
            "AWS_ACCESS_KEY_ID": "testing",
            "AWS_SECRET_ACCESS_KEY": "testing",
            "AWS_SECURITY_TOKEN": "testing",
            "AWS_SESSION_TOKEN": "testing",
            "AWS_DEFAULT_REGION": "us-east-1",
        },
    ):
        yield
