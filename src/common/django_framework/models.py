import uuid

from django.db.models import Model, UUIDField, DateTimeField


class BaseModel(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = DateTimeField(
        auto_now_add=True, verbose_name="Created At", editable=False
    )
    updated_at = DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
