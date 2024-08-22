from typing import Any

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """
    Base schema for all schemas in the project.
    This class is used to define common configurations for all schemas in the project.

    Reference: https://pydantic-docs.helpmanual.io/usage/model_config/
    """

    model_config = ConfigDict(
        populate_by_name=True, use_attribute_docstrings=True, extra="ignore"
    )

    def get(self, item: Any, default: Any = None) -> Any:
        return self.__getitem__(item, default)

    def __getitem__(self, item: Any, default: Any = None) -> Any:
        return getattr(self, item, default)
