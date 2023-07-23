# Python imports
import sys
from os.path import abspath, basename, dirname, join, normpath

from decouple import Csv, config

# ##### PATH CONFIGURATION ################################

# fetch Django's project directory
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# fetch the project_root
PROJECT_ROOT = dirname(DJANGO_ROOT)

# the name of the whole site
SITE_NAME = basename(DJANGO_ROOT)

DEBUG = config("DEBUG", default=False, cast=bool)

if not DEBUG:  # pragma: no cover
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    }

    SESSION_COOKIE_SECURE = True

# collect static files here
STATIC_ROOT = join(PROJECT_ROOT, "run", "static")

# collect media files here
MEDIA_ROOT = join(PROJECT_ROOT, "run", "media")

# look for static assets here
STATICFILES_DIRS = [
    join(PROJECT_ROOT, "static"),
]

# look for templates here
# This is an internal setting, used in the TEMPLATES directive
PROJECT_TEMPLATES = [
    join(PROJECT_ROOT, "templates"),
]

# add apps/ to the Python path
sys.path.append(normpath(join(PROJECT_ROOT, "apps")))

# ##### APPLICATION CONFIGURATION #########################

# these are the apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
]

# Middlewares
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# template stuff
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": PROJECT_TEMPLATES,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    },
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# Internationalization
USE_I18N = False

# Timezone
USE_TZ = False

# ##### SECURITY CONFIGURATION ############################

# We store the secret key here
# The required SECRET_KEY is fetched at the end of this file
SECRET_FILE = normpath(join(PROJECT_ROOT, "run", "SECRET.key"))

# these persons receive error notification
ADMINS = (("Admin", config("DJANGO_SUPERUSER_EMAIL")),)
MANAGERS = ADMINS

# ##### DJANGO RUNNING CONFIGURATION ######################

# the default WSGI application
WSGI_APPLICATION = "%s.wsgi.application" % SITE_NAME

# the root URL configuration
ROOT_URLCONF = "%s.urls" % SITE_NAME

# the URL for static files
STATIC_URL = "/static/"

# the URL for media files
MEDIA_URL = "/media/"

# finally grab the SECRET KEY
try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:  # pragma: no cover
    try:
        from django.utils.crypto import get_random_string

        chars = "abcdefghijklmnopqrstuvwxyz0123456789!$%&()=+-_"
        SECRET_KEY = get_random_string(50, chars)
        with open(SECRET_FILE, "w") as f:
            f.write(SECRET_KEY)
    except IOError:
        raise Exception("Could not open %s for writing!" % SECRET_FILE)

AUTH_USER_MODEL = "users.User"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USERNAME"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOSTNAME"),
        "PORT": 5432,
    }
}

ALLOWED_HOSTS = ["*"]

LOGIN_REDIRECT_URL = "/"

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default=None, cast=Csv())
