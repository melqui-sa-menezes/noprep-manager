from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from apps.drivers.enums import CategoryEnum, FederationEnum
from common.django_framework import BaseModel

__all__ = ["Driver"]

from common.helpers.enums.cities_states import BrazilStatesEnum


class Driver(BaseModel):
    user: User = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='driver',
        help_text=_("Usuário associado ao piloto")
    )
    born_date = models.DateField(help_text=_("Data de nascimento do piloto"))
    city = models.CharField(
        max_length=30,
        help_text=_("Cidade de origem do piloto")
    )
    state = models.CharField(
        max_length=BrazilStatesEnum.get_max_length(),
        help_text=_("Estado de origem do piloto")
    )
    tax_id = models.CharField(
        max_length=11,
        unique=True,
        help_text=_("Documento de indentificação (CPF)")
    )
    license_number = models.CharField(
        max_length=9,
        unique=True,
        blank=True,
        null=True,
        help_text=_("Número da carteira de habilitação")
    )
    category = models.CharField(
        max_length=CategoryEnum.get_max_length(),
        choices=CategoryEnum.get_database_choices(),
        help_text=_("Categoria da licença")
    )
    cba_number = models.CharField(
        max_length=12,
        unique=True,
        blank=True,
        null=True,
        help_text=_("Número de registro CBA")
    )
    federation = models.CharField(
        max_length=FederationEnum.get_max_length(),
        choices=FederationEnum.get_database_choices(),
        help_text=_("Federação de origem do piloto")
    )

    @property
    def user_full_name(self) -> str:
        return self.user.get_full_name()

    @property
    def state_enum(self) -> BrazilStatesEnum | None:
        return BrazilStatesEnum.get(key=self.state, by_value=False, raise_not_found=True)

    @state_enum.setter
    def state_enum(self, state: BrazilStatesEnum) -> None:
        self.state = state.state_symbol

    def __str__(self) -> str:
        if self.federation and self.cba_number:
            return (
                f"{self.user_full_name} "
                f"({FederationEnum(self.federation).federation_symbol} {self.cba_number})"
            )
        return self.user_full_name

    class Meta:
        verbose_name = _("Piloto")
        verbose_name_plural = _("Pilotos")
