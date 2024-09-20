from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.django_framework import BaseModel, AuditMixin
from common.helpers.enums.cities_states import BrazilStatesEnum

__all__ = ["UserProfile"]


class UserProfile(BaseModel, AuditMixin):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    born_date = models.DateField(help_text=_("Data de nascimento do piloto"))
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=30, help_text=_("Cidade de origem do piloto"))
    state = models.CharField(max_length=BrazilStatesEnum.get_max_length(), help_text=_("Estado de origem do piloto"))
    hashed_tax_id = models.CharField(max_length=64, unique=True, help_text=_("Documento de indentificação (CPF)"))
    masked_tax_id = models.CharField(
        max_length=14, blank=True, null=True, help_text=_("Documento de indentificação (CPF) com máscara")
    )

    def __str__(self):
        return self.user.get_full_name()
