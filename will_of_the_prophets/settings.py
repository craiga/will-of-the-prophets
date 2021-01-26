"""Settings."""

import os
import re

import dj_database_url
import django_feature_policy
import django_heroku
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("SECRET_KEY", "placeholder")

DEBUG = bool(os.environ.get("DEBUG", False))

ALLOWED_HOSTS = ["*.herokuapp.com", "localhost"]


# Application definition

INSTALLED_APPS = [
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
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "csp.middleware.CSPMiddleware",
    "django_feature_policy.FeaturePolicyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if bool(os.environ.get("DISABLE_DEBUG_TOOLBAR", False)):
    INSTALLED_APPS.remove("debug_toolbar")
    MIDDLEWARE.remove("debug_toolbar.middleware.DebugToolbarMiddleware")

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
                "will_of_the_prophets.context_processors.sentry_dsn",
            ],
            "string_if_invalid": "ERROR: '%s' is invalid." if DEBUG else "",
        },
    }
]

WSGI_APPLICATION = "will_of_the_prophets.wsgi.application"


# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # https://github.com/jrief/django-sass-processor
    "sass_processor.finders.CssFinder",
]


# Ignore 404s
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-IGNORABLE_404_URLS
IGNORABLE_404_URLS = [re.compile(r"^/phpmyadmin/"), re.compile(r"\.php$")]


# Security
# https://docs.djangoproject.com/en/stable/topics/security/

SECURE_HSTS_SECONDS = 0 if DEBUG else int(os.environ.get("SECURE_HSTS_SECONDS", 60))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"


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

WHITENOISE_ROOT = os.path.join(BASE_DIR, "staticfiles")

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

# Sentry
# https://sentry.io/for/django/

SENTRY_DSN = os.environ.get("SENTRY_DSN", "")

sentry_sdk.init(SENTRY_DSN, integrations=[DjangoIntegration()])


# Content Security Policy
# https://django-csp.readthedocs.io/en/latest/configuration.html

CSP_STYLE_SRC = ["'self'", "cdnjs.cloudflare.com"]
CSP_IMG_SRC = ["'self'", "s3.amazonaws.com", "s3.us-east-1.amazonaws.com"]
CSP_SCRIPT_SRC = ["'self'", "browser.sentry-cdn.com", "cdnjs.cloudflare.com"]
CSP_CONNECT_SRC = ["'self'", "s3.us-east-1.amazonaws.com"]
CSP_REPORT_ONLY = bool(os.environ.get("CSP_REPORT_ONLY", DEBUG))
CSP_REPORT_URI = os.environ.get("CSP_REPORT_URI", None)
CSP_INCLUDE_NONCE_IN = ["script-src", "style-src"]


# Feature policy
# https://github.com/adamchainz/django-feature-policy#setting

FEATURE_POLICY = {
    feature_name: "none" for feature_name in django_feature_policy.FEATURE_NAMES
}
FEATURE_POLICY["document-domain"] = "self"


PUBLIC_BOARD_CANONICAL_URL = os.environ.get("PUBLIC_BOARD_CANONICAL_URL")


# Inject settings for Heroku.
django_heroku.settings(locals())


if os.environ.get("DATABASE_NO_SSL_REQUIRE"):
    DATABASES["default"] = dj_database_url.config(ssl_require=False)
