from .base import *
from pathlib import Path
from dotenv import load_dotenv
import os

# Environment load from .env file
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(env_path)

SECRET_KEY = ^52vdq+*6n#ygj&ip&1a5m24l4hodn@5f*8gcl7+4r*8f!-^f=-b^ev8ti_f5-xz=le3$i&aqa(tbz&xdfa52_vl0nyu9-mng09s
DEBUG = False

ALLOWED_HOSTS = []

if os.getenv("DATABASE_NAME"):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv("DATABASE_NAME"),
            'USER': os.getenv("DATABASE_USER"),
            'PASSWORD': os.getenv("DATABASE_PASSWORD"),
            'HOST': os.getenv("DATABASE_HOST"),
            'PORT': os.getenv("DATABASE_PORT"),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }