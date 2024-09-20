from django.db import models

from common.django_framework import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


__all__ = ["EventType", "Event", "Subscription"]


class EventType(BaseModel):
    name = models.CharField(max_length=30, help_text=_("Nome do tipo de Evento"), verbose_name=_("Nome"))
    description = models.CharField(
        max_length=200, blank=True, null=True, help_text=_("Descrição do tipo de Evento"), verbose_name=_("Descrição")
    )

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = _("Tipo de Evento")
        verbose_name_plural = _("Tipos de Eventos")


class Event(BaseModel):
    name = models.CharField(max_length=100, help_text=_("Nome do evento"))
    date = models.DateField(help_text=_("Data do Evento"))
    starts_at = models.TimeField(blank=True, null=True, help_text=_("Horário de Início do Evento"))
    ends_at = models.TimeField(blank=True, null=True, help_text=_("Horário de Término do Evento"))
    address = models.CharField(max_length=256, help_text=_("Endereço do Evento"))
    fee = models.DecimalField(
        decimal_places=2, max_digits=7, blank=True, null=True, help_text=_("Taxa de inscrição do Evento")
    )
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, max_length=100, help_text=_("Organizador do Evento"))
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, help_text=_("Tipo de Evento"))
    regulation = models.URLField(
        max_length=200, blank=True, null=True, help_text=_("Acesso ao link do regulamento do Evento")
    )

    class Meta:
        verbose_name = _("Evento")
        verbose_name_plural = _("Eventos")

    def __str__(self) -> str:
        return f"{self.name}"


class Subscription(BaseModel):
    driver = models.ForeignKey(
        "drivers.Driver",
        on_delete=models.CASCADE,
        related_name="subscriptions",
        help_text=_("Piloto inscrito no evento"),
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        help_text=_("Evento ao qual o piloto se inscreveu"),
    )
    subscription_date = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Data e hora da inscrição"),
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", _("Pendente")),
            ("confirmed", _("Confirmada")),
            ("canceled", _("Cancelada")),
        ],
        default="pending",
        help_text=_("Status da inscrição"),
    )

    class Meta:
        verbose_name = _("Inscrição")
        verbose_name_plural = _("Inscrições")
        unique_together = ("driver", "event")
        ordering = ["-subscription_date"]

    def __repr__(self) -> str:
        return f"{self.driver} - {self.event.name}"
