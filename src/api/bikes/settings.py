import os
import sys
import time
from pathlib import Path

import corsheaders.defaults
from drf_yasg import openapi

from bikes.constants import Environment


class DisableCSRFMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, "_dont_enforce_csrf_checks", True)
        response = self.get_response(request)
        return response


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "aaa")
DEBUG = os.getenv("DEBUG", "false") == "true"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
ADDITIONAL_ALLOWED_HOSTS = [
    a for a in os.getenv("ADDITIONAL_ALLOWED_HOSTS", "").split(",") if a
]
ALLOWED_HOSTS.extend(ADDITIONAL_ALLOWED_HOSTS)
print(
    f"ALLOWED_HOSTS: {ALLOWED_HOSTS} - ADDITIONAL_ALLOWED_HOSTS: {ADDITIONAL_ALLOWED_HOSTS}"
)

ENVIRONMENT = Environment(os.getenv("ENVIRONMENT", "prod"))

TESTING = False
if (
    "django_test_manage.py" in sys.argv[0]
    or ("manage.py" in sys.argv[0] and "test" in sys.argv)
    or "coverage" == sys.argv[0]
):
    TESTING = True
    ENVIRONMENT = Environment("test")

INSTALLED_APPS = [
    "psqlextra",
    # "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    # "django.contrib.messages",
    "django.contrib.staticfiles",
    "health_check",  # required
    "health_check.db",  # stock Django health checkers
    # 'health_check.cache',
    # 'health_check.storage',
    "health_check.contrib.migrations",
    "health_check.contrib.psutil",  # disk and memory utilization; requires psutil
    "django_extensions",
    "corsheaders",
    "drf_yasg",
    "rest_framework",
    "django_filters",
    "bikes",
]

AWS_REGION = "us-west-1"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "bikes.settings.DisableCSRFMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "bikes.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                # "django.contrib.auth.context_processors.auth",
                # "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "bikes.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": 5432,
    },
    "readonly": {
        "ENGINE": "psqlextra.backend",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER_READONLY"),
        "PASSWORD": os.getenv("DB_PASSWORD_READONLY"),
        "HOST": os.getenv("DB_HOST_READONLY"),
        "PORT": 5432,
    },
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
APPEND_SLASH = False

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s]: %(message)s",
            "style": "%",
            "converter": time.gmtime,
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
        "": {  # 'catch all' loggers by referencing it with the empty string
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
    },
}

HEALTH_CHECK = {
    "DISK_USAGE_MAX": 90,  # percent
    "MEMORY_MIN": 100,  # in MB
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5000",
    "https://bikes.rustybrooks.com",
    "https://bikes.rustybrooks.net",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [*corsheaders.defaults.default_headers]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5000",
    "https://bikes.rustybrooks.com",
    "https://bikes.rustybrooks.net",
]

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
}

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# FIXME
STATIC_ROOT = "/tmp/static/"
