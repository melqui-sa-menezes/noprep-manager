from django.db.models import Model, ForeignKey, SET_NULL
from django.contrib.auth.models import User


class AuditMixin(Model):
    created_by = ForeignKey(
        User,
        related_name="%(class)s_created",
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    updated_by = ForeignKey(
        User,
        related_name="%(class)s_updated",
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
