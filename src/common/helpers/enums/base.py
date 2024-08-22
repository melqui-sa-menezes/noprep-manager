from enum import Enum
from typing import Any, TypeVar, NamedTuple, Generic, Iterable, Self

__all__ = ["BaseEnum", "InsensitiveCaseEnum"]

T = TypeVar("T", bound=Any)


class DatabaseChoices(NamedTuple, Generic[T]):
    key: T
    value: T


class BaseEnum(Enum):
    @classmethod
    def get_database_choices(cls, by_name: bool = False) -> Iterable[tuple[DatabaseChoices, ...]]:
        if by_name:
            return tuple(DatabaseChoices(item.name, item.value) for item in cls)
        return tuple(DatabaseChoices(item.value, item.value) for item in cls)

    @classmethod
    def get_max_length(cls) -> int:
        return max(map(lambda item: len(item.value), cls))

    @classmethod
    def get_values(cls) -> list[str]:
        return [key.value for key in cls]

    @classmethod
    def get_names(cls) -> list[str]:
        return [key.name for key in cls]

    @classmethod
    def to_dict(cls) -> dict:
        return dict(map(lambda item: (item.name, item.value), cls))

    @classmethod
    def _missing_(cls, value: Any) -> Any:
        for member in cls:
            if member.value == value:
                return member
        return None

    @classmethod
    def get(
        cls,
        key: object | str,
        default: T | None = None,
        *,
        by_value: bool = False,
        raise_not_found: bool = False,
    ) -> Self | T | None:
        try:
            if by_value is True:
                return cls(key)
            return cls[str(key).upper()]
        except (ValueError, KeyError) as error:
            if raise_not_found:
                raise ValueError(str(error)) from error
            return default


class InsensitiveCaseEnum(str, BaseEnum):
    @classmethod
    def _missing_(cls, value: Any) -> Any:
        for member in cls:
            if str(member.value).lower() == str(value).lower():
                return member
        return None
