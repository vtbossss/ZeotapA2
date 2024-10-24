"""
Django settings for weather_monitoring project.

Generated by 'django-admin startproject' using Django 4.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os  # Import os for environment variable management
from dotenv import load_dotenv  # Import dotenv to load environment variables

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Load environment variables from .env file
load_dotenv()

# Fetch the API key and Django secret key from the environment
API_KEY = os.getenv('OPENWEATHER_API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

# Raise an error if the API key or secret key is not found
if API_KEY is None:
    raise ValueError("API key not found. Please set the OPENWEATHER_API_KEY environment variable.")

if SECRET_KEY is None:
    raise ValueError("Django secret key not found. Please set the DJANGO_SECRET_KEY environment variable.")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Specify allowed hosts
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "weather",  # Include the 'weather' app
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URL configuration module
ROOT_URLCONF = "weather_monitoring.urls"

# Template settings
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],  # Specify template directories
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

# WSGI application configuration
WSGI_APPLICATION = "weather_monitoring.wsgi.application"

# Database settings
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # Use SQLite as the database engine
        "NAME": BASE_DIR / "db.sqlite3",  # Database file location
    }
}

# Password validation settings
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization settings
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"  # Set timezone
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images) settings
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Celery configuration
CELERY_BROKER_URL = 'redis://redis:6379/0'  # URL for the Celery broker (Redis)
#CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Uncomment for local Redis setup

CELERY_ACCEPT_CONTENT = ['json']  # Specify accepted content types
CELERY_TASK_SERIALIZER = 'json'  # Specify task serialization format

from celery.schedules import crontab  # Import crontab for task scheduling

# Define the Celery beat schedule for periodic tasks
CELERY_BEAT_SCHEDULE = {
    'fetch-weather-every-1-minutes': {
        'task': 'weather.tasks.periodic_weather_update',  # Specify the task to run
        'schedule': crontab(minute='*/1'),  # Schedule to run every minute
    },
}
