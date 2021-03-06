"""
Django settings for settings project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, "static/")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-yg7m(0489_ofj6z#%tr)!h#7=hbz4!dgr$fq1g=4g!vagw!jlf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.humanize",

    "corsheaders",
    "rest_framework",

    'authApp',
    'coreApp',
    'clientApp',
    'organisationApp',
    'productionApp',
    'commandeApp',
    'livraisonApp',
    'approvisionnementApp',
    'ficheApp',
    'comptabilityApp',
    'paramApp',
    'administrationApp'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    "django.middleware.common.CommonMiddleware",
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'coreApp.middleware.LockoutMiddleware',
    'coreApp.middleware.AccessCheckMiddleware',
    'paramApp.middleware.InjectMyAppDataMiddleware',
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'settings.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bricx',
        'USER': 'root',
        'PASSWORD': '12345678',
        'HOST': '172.17.0.4',
        'PORT': '3306',
    },
    
    #     'default': {
    #     'ENGINE': 'django_yugabytedb',
    #     'HOST': '172.17.0.3',
    #     'PORT': 5433,
    #     'NAME': 'yuga_db',
    #     'USER': 'admin',
    #     'PASSWORD': 'yugabyte',
    # },

    # 'sqlite': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'dba.sqlite3',
    # }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('fr', 'Fran??ais'),
    # ('en_GB', 'English (US)'),
    ('tr', 'Turkish'),
    ('ar', '????????'),
)

print(BASE_DIR)
LOCALE_PATHS = (
   os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CORS_ALLOW_ALL_ORIGINS = True


LOGIN_URL = "/auth/"

SESSION_ENGINE = 'django.contrib.sessions.backends.db'   # Engine (default)
SESSION_COOKIE_NAME = "sessionid"                       #  Session's cookie is saved on the browser, namely: sessionId = random string (default)
SESSION_COOKIE_PATH = "/"                               #  Session's cookie saved path (default)
SESSION_COOKIE_DOMAIN = None                             #  Session's cookie saved domain (default)
SESSION_COOKIE_SECURE = False                            #  Whether HTTPS is transferred for cookies (default)
SESSION_COOKIE_HTTPONLY = True                           #  Whether the session's cookie only supports HTTP transmission (default)
SESSION_COOKIE_AGE = 1209600                             #  Session's cookie failure date (2 weeks) (default)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False                  #  Whether to close your browser makes the session expire (default)
SESSION_SAVE_EVERY_REQUEST = True  