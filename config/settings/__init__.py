import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(env_path)

DJANGO_ENV = os.environ.get("DJANGO_ENV", "dev")

if os.environ.get("DJANGO_ENV") == "prod":
    from .prod import *  # noqa: F401,F403
else:
    from .dev import *  # noqa: F401,F403