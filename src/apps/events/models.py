from tkinter.font import names

from django.db import models
from common.django_framework import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User



class EventType(BaseModel):
    name = models.CharField(max_length=30, help_text=_("Nome do tipo de Evento"))
    description = models.CharField(max_length=200, blank=True, null=True, help_text=_("Descrição de Evento"))

    def __str__(self) -> str:
        return f"{self.name}"


class Event(BaseModel):
    name = models.CharField(max_length=100, help_text=_("Nome do evento"))
    date = models.DateField(help_text=_("Data do Evento"))
    starts_at = models.TimeField(blank=True, null=True, help_text=_("Horário de Início do Evento"))
    ends_at = models.TimeField(blank=True, null=True, help_text=_("Horário de Término do Evento"))
    address = models.CharField(max_length=256, help_text=_("Endereço do Evento"))
    fee = models.DecimalField(decimal_places=2, max_digits= 7, blank=True, null=True, help_text=_("Taxa de inscrição do Evento"))
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, max_length=100, help_text=_("Organizador do Evento"))
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, help_text=_("Tipo de Evento"))
    regulation = models.URLField(max_length=200, blank=True, null=True, help_text=_("Acesso ao link do regulamento do Evento"))
