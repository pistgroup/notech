"""
Django settings for my_project project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
'''BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))'''
#Templatesをappsごとではなくprojects単体で管理するためBASE_DIRSを追加
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u-1gug41k)qs4pw)n=qq(u4@g8#fp52*9^c^h5+hc3h-8pczyd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'reversion', #履歴管理
    'stdimage',
    'cart.apps.CartConfig',
    'accounts.apps.AccountsConfig',
    'my_apps.apps.MyAppsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'my_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #Templatesをappsごとではなくprojects単体で管理するためDIRSにパスを追加
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'my_apps.context_parts.common',
                'cart.context_data.counter',
            ],

        },
    },
]

WSGI_APPLICATION = 'my_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    # pymysqlをインストール
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'notech',  # 作成したデータベース名 ローカルmac create database
        'USER': 'root',  # ログインユーザー名
        'HOST': '',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# ログイン後トップページにリダイレクト
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'my_apps:mypage'

# ログイン機能のユーザーモデルを定義
AUTH_USER_MODEL = 'accounts.User'

# メディア
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# メールをコンソールに表示する
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#Stripe API
STRIPE_PUBLIC_KEY = 'pk_test_pukTGyXS6Uv4tpqjoRME5L5900keuWYsW7'
STRIPE_SECRET_KEY = 'sk_test_J6A1KYV2dyogayCuOBJHFT5t00TCFVRj9L'