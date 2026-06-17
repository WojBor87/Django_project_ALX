from .base import *
from pathlib import Path
from dotenv import load_dotenv
import os

# Environment load from .env file
env_path = Path(__file__).resolve().parent.parent.parent / '.env_test'
load_dotenv(env_path)

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG')
HOSTS = os.getenv('ALLOWED_HOSTS')

ALLOWED_HOSTS = [HOSTS]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}
