"""
Django settings for MamaPesa project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import redis
from urllib.parse import urlparse
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
redis_url = urlparse(os.environ.get('REDISCLOUD_URL'))
# r = redis.Redis(host=redis_url.hostname, port=redis_url.port, password=redis_url.password)
# print("Redis cloud url: ", redis_url)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7_0r_pc^w1p5ho9wfw3ep)u8(^grx2486f7824^_)df3dbz$^_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True").lower() in ['true', '1', 't', 'yes', 'y']

ALLOWED_HOSTS = ['softconnect-ce8065bce25a.herokuapp.com',
                 '127.0.0.1',
                 'softconnectai.tech',
                 'anthony001.pythonanywhere.com']


# Application definition

INSTALLED_APPS = [
    # 'daphne',
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'main.apps.MainConfig',
    #'mpesa_api',
    'chatbot.apps.ChatbotConfig',
    'vision.apps.VisionConfig',
    'auth0.apps.Auth0Config',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MamaPesa.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MamaPesa.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True
X_FRAME_OPTIONS = 'SAMEORIGIN'

CACHES = {
    'default': {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        #'LOCATION': '127.0.0.1:11211',  # Memcached server address
    }
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/'), ]
STATIC_ROOT = BASE_DIR / "staticfiles"
#STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STORAGES = {
    "default":{
        "BACKEND": "django.core.files.storage.FileSystemStorage"
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

ASGI_APPLICATION = "MamaPesa.asgi.application"

CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
            },
        },
    }
# if DEBUG:
#     CHANNEL_LAYERS = {
#         "default": {
#             "BACKEND": "channels_redis.core.RedisChannelLayer",
#             "CONFIG": {
#                 "hosts": [("127.0.0.1", 6379)],
#             },
#         },
#     }
# else:
#     CHANNEL_LAYERS = {
#         "default": {
#             "BACKEND": "channels_redis.core.RedisChannelLayer",
#             # "CONFIG": {
#             #     "hosts": [f"redis://:{redis_url.password}@{redis_url.hostname}:{redis_url.port}/{redis_url.path.lstrip('/')}"],
#             # },
#             'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
#             'OPTIONS': {
#                 'PASSWORD': redis_url.password,
#                 "ssl_cert_reqs": None,
#                 'DB': 0,
#             }
#         },
#     }

    # Example for using redis_cache.RedisCache if required
    # CACHES = {
    #     'default': {
    #         'BACKEND': 'redis_cache.RedisCache',
    #         'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
    #         'OPTIONS': {
    #             'PASSWORD': redis_url.password,
    #             'DB': 0,
    #         }
    #     }
    # }
