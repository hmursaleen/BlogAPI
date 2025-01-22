"""
Django settings for blog_api project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5d_i_-^)v#8)pp9*@2qes*!u(c+!)8go4y^^138xpp*lm7xcp$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'blog.apps.BlogConfig',
    'drf_yasg',
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

ROOT_URLCONF = 'blog_api.urls'

# Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

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

WSGI_APPLICATION = 'blog_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''

'''
Django requires a valid DATABASES entry, even if you're not using the ORM.
This provides a valid database engine and an in-memory database that won't persist data or 
interfere with your PyMongo operations.
Django's test framework and certain internal mechanisms require a valid DATABASES configuration.
Using SQLite with an in-memory database:
Satisfies Django's requirements for a database engine.
Ensures no real database is used, keeping the focus on MongoDB.
'''

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",  # In-memory database for tests and compatibility
    }
}


'''
Since PyMongo is not an ORM, you cannot use Django's DATABASES setting for MongoDB. Instead, 
you'll establish a connection manually.

Unlike relational databases, MongoDB doesn’t require migrations. Collections and documents 
are created dynamically as data is inserted. The BlogPost model will interact directly with 
MongoDB without migration steps.
'''

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

# MongoDB Configuration
MONGO_HOST = "localhost"  
MONGO_PORT = 27017        
MONGO_DB_NAME = "blog_db"
MONGO_USERNAME = None
MONGO_PASSWORD = None
MONGO_URI = 'mongodb://localhost:27017/'


# Create MongoDB client
mongo_client = MongoClient(
    host=MONGO_HOST,
    port=MONGO_PORT,
    username=MONGO_USERNAME,
    password=MONGO_PASSWORD,
    serverSelectionTimeoutMS=5000,
)

# Access the database
mongo_db = mongo_client[MONGO_DB_NAME]

try:
    mongo_client.admin.command("ping")
    print("MongoDB connection established successfully!")
except ServerSelectionTimeoutError as e:
    print(f"Error: Unable to connect to MongoDB: {e}")



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
