"""
Django settings for escolares project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from django.urls import reverse_lazy
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)vt#jee#=#h246r6b4+udt2%7u$f12+qo0&$sbxks52he78))x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.1.4']


# Application definition

PROJECTS_APPS = [
    'apps.clientes.familias',
    'apps.clientes.adultos',
    'apps.clientes.estudiantes',
    'apps.clientes.direcciones',
    'apps.empleados',
    'apps.vehiculos',
    'apps.recorridos',
    'apps.login',
    'apps.home',
    'apps.contabilidad.ingresos',
    'apps.contabilidad.gastos',
    'apps.contabilidad.precios',
    'apps.contabilidad.sueldos',
    ]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ]

INSTALLED_APPS = DJANGO_APPS + PROJECTS_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'escolares.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR,'apps/login/templates'),
            os.path.join(BASE_DIR,'apps/clientes/familias/templates'),
            os.path.join(BASE_DIR,'apps/empleados/templates'),
            os.path.join(BASE_DIR,'apps/vehiculos/templates'),
            os.path.join(BASE_DIR,'apps/recorridos/templates'),
            os.path.join(BASE_DIR,'apps/contabilidad/ingresos/templates'),
            ],
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

WSGI_APPLICATION = 'escolares.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'escolares_db',
        'USER':'postgres',
        'PASSWORD':'1610',
        'HOST':'127.0.0.1',
        'DATABASE_PORT':'5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOGIN_REDIRECT_URL = reverse_lazy('inicio')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'apps/login/static'),
    os.path.join(BASE_DIR, 'apps/clientes/familias/static'),
    os.path.join(BASE_DIR, 'apps/empleados/static'),
    os.path.join(BASE_DIR, 'apps/vehiculos/static'),
    os.path.join(BASE_DIR, 'apps/recorridos/static'),
    os.path.join(BASE_DIR, 'apps/contabilidad/ingresos/static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
