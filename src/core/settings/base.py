import os
import socket
import uuid

import dj_database_url
from simple_settings.strtobool import strtobool


VERSION = "0.1.0"
APP_NAME = "noprep-manager"
ENVIRONMENT = os.getenv("SIMPLE_SETTINGS", "undefined").split(".")[-1:][0]
PROCESS_TYPE = os.getenv("PROCESS_TYPE", "undefined")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
CORE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(CORE_DIR)
SRC_DIR = os.path.dirname(PROJECT_DIR)
BASE_DIR = os.path.dirname(SRC_DIR)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", str(uuid.uuid4()))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.getenv("DEBUG", "False"))

# DJANGO SETTINGS
# https://docs.djangoproject.com/en/5.0/ref/settings/

# Apps settings
DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "import_export",
    "django_extensions",
    "corsheaders",
]

LOCAL_APPS = [
    "core",
    "apps.drivers.apps.DriversConfig",
    "apps.events.apps.EventsConfig",
    "apps.user_profiles.apps.UserProfilesConfig",
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware settings
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

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
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
ROOT_URLCONF = "urls"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASE_URL = os.getenv("DATABASE_URL", "postgres://postgres:postgres@127.0.0.1:5432/noprep-manager")
DATABASE_READ_URL = os.getenv("DATABASE_READ_URL", DATABASE_URL)
DATABASE_APPLICATION_NAME = (
    f"{PROCESS_TYPE.upper()} {ENVIRONMENT.title()} {VERSION} - PID {os.getpid()} <{socket.gethostname()}>"[:63]
)

DATABASES = {
    "default": dj_database_url.parse(
        url=DATABASE_URL + f"?application_name={DATABASE_APPLICATION_NAME}",
        engine="django.db.backends.postgresql",
        conn_max_age=int(os.getenv("DATABASE_CONN_MAX_AGE", "600")),
        ssl_require=strtobool(os.getenv("DATABASE_SSL_REQUIRE", "False")),
    ),
    "default_read": dj_database_url.parse(
        url=DATABASE_READ_URL + f"?application_name={DATABASE_APPLICATION_NAME}",
        engine="django.db.backends.postgresql",
        conn_max_age=int(os.getenv("DATABASE_CONN_MAX_AGE", "600")),
        ssl_require=strtobool(os.getenv("DATABASE_SSL_REQUIRE", "False")),
    ),
}

DATABASE_ROUTERS = ["core.routers.DatabaseRouter"]


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
