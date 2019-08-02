"""Settings."""

import os
import re

import dj_database_url
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("SECRET_KEY", "placeholder")

DEBUG = bool(os.environ.get("DEBUG", False))

ALLOWED_HOSTS = ["*.herokuapp.com", "localhost"]


# Application definition

INSTALLED_APPS = [
    "raven.contrib.django.raven_compat",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sass_processor",
    "widget_tweaks",
    "tz_detect",
    "debug_toolbar",
    "s3direct",
    "will_of_the_prophets",
]

MIDDLEWARE = [
    "raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
]

ROOT_URLCONF = "will_of_the_prophets.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "string_if_invalid": "ERROR: '%s' is invalid." if DEBUG else "",
        },
    }
]

WSGI_APPLICATION = "will_of_the_prophets.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        )
    },
    {"NAME": ("django.contrib.auth.password_validation" ".MinimumLengthValidator")},
    {"NAME": ("django.contrib.auth.password_validation" ".CommonPasswordValidator")},
    {"NAME": ("django.contrib.auth.password_validation" ".NumericPasswordValidator")},
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # https://github.com/jrief/django-sass-processor
    "sass_processor.finders.CssFinder",
]


# Ignore 404s
# https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-IGNORABLE_404_URLS
IGNORABLE_404_URLS = [re.compile(r"^/phpmyadmin/"), re.compile(r"\.php$")]


# Logging
# Combination of logging settings from https://github.com/heroku/django-heroku/
# and https://docs.sentry.io/clients/python/integrations/django/.

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "WARNING", "handlers": ["sentry"]},
    "formatters": {
        "heroku": {
            "format": (
                "%(asctime)s [%(process)d] [%(levelname)s] "
                + "pathname=%(pathname)s lineno=%(lineno)s "
                + "funcname=%(funcName)s %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "sentry": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
        "sentry": {
            "level": "WARNING",
            "class": ("raven.contrib.django.raven_compat.handlers" ".SentryHandler"),
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "heroku",
        },
    },
    "loggers": {
        "raven": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
        "sentry.errors": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "testlogger": {"handlers": ["console"], "level": "INFO"},
    },
}


# Security
# https://docs.djangoproject.com/en/2.2/topics/security/

SECURE_HSTS_SECONDS = 0 if DEBUG else 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"


# django-sass-processor
# https://github.com/jrief/django-sass-processor

SASS_OUTPUT_STYLE = "compressed"


# django-tz-detect
# https://github.com/adamcharnock/django-tz-detect

MIDDLEWARE += ["tz_detect.middleware.TimezoneMiddleware"]

TZ_DETECT_COUNTRIES = ("US", "CN", "IN", "JP", "BR", "RU", "DE", "FR", "GB")


# django-debug-toolbar
# https://django-debug-toolbar.readthedocs.io/en/stable/installation.html

INTERNAL_IPS = ("127.0.0.1",)


# Whitenoise
# http://whitenoise.evans.io/en/stable/django.html#available-settings

WHITENOISE_ROOT = os.path.join(BASE_DIR, "static")

# django-s3direct
# https://github.com/bradleyg/django-s3direct

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL")
S3DIRECT_DESTINATIONS = {
    "special_square": {"key": "special_squares/", "auth": lambda u: u.is_staff}
}


# Content Security Policy
# https://django-csp.readthedocs.io/en/latest/configuration.html

CSP_REPORT_ONLY = True
CSP_REPORT_URI = os.environ.get("CSP_REPORT_URI", None)


PUBLIC_BOARD_CANONICAL_URL = os.environ.get("PUBLIC_BOARD_CANONICAL_URL")

# Inject settings for Heroku.
django_heroku.settings(locals(), logging=False)


if os.environ.get("DATABASE_NO_SSL_REQUIRE"):
    DATABASES["default"] = dj_database_url.config(ssl_require=False)
