import uuid
from typing import TypeVar, Generic, Self

from django.db.models import Model, UUIDField, DateTimeField, QuerySet
from django.db.models.sql import Query

_BaseModel_co = TypeVar("_BaseModel_co", bound="BaseModel", covariant=True)


class ObjectsQuerySet(QuerySet, Generic[_BaseModel_co]):
    model: _BaseModel_co
    query: Query

    def __init__(
        self,
        model: _BaseModel_co | None = None,
        query: Query | None = None,
        using: str | None = None,
        hints: dict | None = None,
    ):
        if query is None:
            query = Query(model)

        super().__init__(model=model, query=query, using=using, hints=hints)


class BaseModel(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = DateTimeField(auto_now_add=True, verbose_name="Created At", editable=False)
    updated_at = DateTimeField(auto_now=True, verbose_name="Updated At")

    objects: ObjectsQuerySet[Self] = ObjectsQuerySet.as_manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
