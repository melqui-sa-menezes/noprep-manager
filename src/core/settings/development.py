from .base import *  # noqa:F403

DEBUG = strtobool(os.getenv("DEBUG", "True"))  # noqa:F405
SECRET_KEY = os.getenv(  # noqa:F405
    "SECRET_KEY", "6da2f28f-f6fd-432e-be1e-9d11b3fc5f3e"
)
