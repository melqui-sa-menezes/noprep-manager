from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from apps.drivers.enums import CategoryEnum, FederationEnum
from common.django_framework import BaseModel
from common.helpers.enums.cities_states import BrazilStatesEnum

__all__ = ["Driver"]


class Driver(BaseModel):
    user: User = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="driver", help_text=_("Usuário associado ao piloto")
    )
    nickname = models.CharField(max_length=32, blank=True, null=True, help_text=_("Apelido do piloto"))
    born_date = models.DateField(help_text=_("Data de nascimento do piloto"))
    city = models.CharField(max_length=30, help_text=_("Cidade de origem do piloto"))
    state = models.CharField(max_length=BrazilStatesEnum.get_max_length(), help_text=_("Estado de origem do piloto"))
    hashed_tax_id = models.CharField(max_length=64, unique=True, help_text=_("Documento de indentificação (CPF)"))
    masked_tax_id = models.CharField(
        max_length=14, blank=True, null=True, help_text=_("Documento de indentificação (CPF) com máscara")
    )
    license_number = models.CharField(
        max_length=9, blank=True, null=True, help_text=_("Número da carteira de habilitação")
    )
    category = models.CharField(
        max_length=CategoryEnum.get_max_length(),
        choices=CategoryEnum.get_database_choices(),
        help_text=_("Categoria da licença"),
    )
    cba_number = models.CharField(
        max_length=12, blank=True, null=True, help_text=_("Número de registro CBA")
    )
    federation = models.CharField(
        max_length=FederationEnum.get_max_length(),
        choices=FederationEnum.get_database_choices(),
        help_text=_("Federação de origem do piloto"),
    )

    @property
    def user_full_name(self) -> str:
        if self.nickname:
            return f'{self.user.first_name} "{self.nickname}" {self.user.last_name}'
        return self.user.get_full_name()

    @property
    def state_enum(self) -> BrazilStatesEnum | None:
        return BrazilStatesEnum.get(key=self.state, by_value=False, raise_not_found=True)

    @state_enum.setter
    def state_enum(self, state: BrazilStatesEnum) -> None:
        self.state = state.state_symbol

    def __str__(self) -> str:
        if self.federation and self.cba_number:
            return f"{self.user_full_name} " f"({FederationEnum(self.federation).federation_symbol} {self.cba_number})"
        return self.user_full_name

    class Meta:
        verbose_name = _("Piloto")
        verbose_name_plural = _("Pilotos")

        constraints = [
            models.UniqueConstraint(
                fields=["license_number"],
                name="unique_license_number",
                condition=~Q(license_number__isnull=True),
            ),
            models.UniqueConstraint(
                fields=["cba_number"],
                name="unique_cba_number",
                condition=~Q(cba_number__isnull=True),
            )
        ]

class Vehicle(BaseModel):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, help_text=_("Piloto relacionado ao Veículo"))
    registration_number = models.CharField(max_length=12, unique=True, help_text=_("Número de Registro do Veículo"))
    brand = models.CharField(max_length=30, help_text=_("Marca do veículo"))
    model = models.CharField(max_length=30, help_text=_("Modelo do veículo"))
    manufacture_year = models.IntegerField(help_text=_("Ano de Fabricação do veículo"))
    chassis_number = models.CharField(max_length=17, unique=True, help_text=_("Número de identificação do chassi"))
    plate_number = models.CharField(max_length=8, unique=True, help_text=_("Placa de identificação do veículo"))
    color = models.CharField(max_length=20, help_text=_("Cor do veículo"))
    fuel_type = models.CharField(max_length=20, help_text=_("Tipo de combustível (Gasolina, Diesel, Elétrico, etc.)"))
    current_owner = models.CharField(max_length=50, help_text=_("Nome do proprietário atual do veículo"))
    insured = models.BooleanField(default=False, help_text=_("Se o veículo possui seguro (Sim/Não)"))

class RaceHistory(BaseModel):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, help_text=_("Piloto relacionado ao histórico"))new
    event_name = models.CharField(max_length=100, help_text=_("Nome do evento ou corrida"))
    date = models.DateField(help_text=_("Data da corrida"))
    position = models.IntegerField(help_text=_("Posição alcançada na corrida"))
    time = models.DurationField(blank=True, null=True, help_text=_("Tempo total da corrida"))
