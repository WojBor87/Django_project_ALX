from .base import *
from pathlib import Path
from dotenv import load_dotenv
import os

# Environment load from .env file
env_path = Path(__file__).resolve().parent.parent.parent / '.env_test'
load_dotenv(env_path)

SECRET_KEY = os.getenv('SECRET_KEY')
HOSTS = os.getenv('ALLOWED_HOSTS')

ALLOWED_HOSTS = [HOSTS]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'production': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}
