import pytest
from simple_settings import LazySettings

from src.common.helpers.utils.hash import hash_data, validate_hash


@pytest.fixture(autouse=True)
def fake_settings():
    fake_settings = LazySettings()
    fake_settings.__setattr__("SECRET_KEY", "my_secret")
    yield fake_settings


class TestHashData:
    def test_hash_typical_string(self):
        # Act
        result = hash_data("test_value")

        # Assert
        assert result == "0767be3f4c1a85fbe83125ff703fbd382e01d10bd32787e3204c66c9826c80b7"

    def test_hash_empty_string(self):
        # Act
        result = hash_data("")

        # Assert
        assert result == ""


class TestValidateHash:

    def test_validate_correct_value(self):
        # Arrange
        value = "test_value"
        hashed_value = hash_data(value)

        # Act
        result = validate_hash(value, hashed_value)

        # Assert
        assert result is True

    def test_validate_very_long_string(self):
        # Arrange
        value = "a" * 10000
        hashed_value = hash_data(value)

        # Act
        result = validate_hash(value, hashed_value)

        # Assert
        assert result is True
