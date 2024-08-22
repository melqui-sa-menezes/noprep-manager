import hmac
import hashlib
from simple_settings import settings


def hash_data(value: str) -> str:
    """
    Hash data using the SECRET_KEY from settings.

    Args:
        value (str): The value to be hashed.

    Return:
        str: The hashed value.
    """
    if not value:
        return value
    secret = settings.SECRET_KEY.encode("utf-8")
    return hmac.new(secret, value.encode("utf-8"), hashlib.sha256).hexdigest()


def validate_hash(value: str, hashed_value: str) -> bool:
    """
    Validate if the value is equal to the hashed value.

    Args:
        value (str): The value to be validated.
        hashed_value (str): The hashed value to be compared.

    Return:
        bool: True if the value is equal to the hashed value, False otherwise.
    """
    return hmac.compare_digest(hash_data(value), hashed_value)
