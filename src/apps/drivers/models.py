from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from apps.drivers.enums import CategoryEnum, FederationEnum
from apps.user_profiles.models import UserProfile
from common.django_framework import BaseModel
from common.helpers.enums.cities_states import BrazilStatesEnum

__all__ = ["Driver", "Vehicle", "RaceHistory", "LapTime"]


class Driver(BaseModel):
    user: UserProfile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="driver", help_text=_("Usuário associado ao piloto")
    )
    nickname = models.CharField(max_length=32, blank=True, null=True, help_text=_("Apelido do piloto"))
    license_number = models.CharField(
        max_length=9, blank=True, null=True, help_text=_("Número da carteira de habilitação")
    )
    category = models.CharField(
        max_length=CategoryEnum.get_max_length(),
        choices=CategoryEnum.get_database_choices(),
        help_text=_("Categoria da licença"),
    )
    cba_number = models.CharField(max_length=12, blank=True, null=True, help_text=_("Número de registro CBA"))
    federation = models.CharField(
        max_length=FederationEnum.get_max_length(),
        choices=FederationEnum.get_database_choices(),
        help_text=_("Federação de origem do piloto"),
    )

    @property
    def state_enum(self) -> BrazilStatesEnum | None:
        return BrazilStatesEnum.get(key=self.state, by_value=False, raise_not_found=True)

    @state_enum.setter
    def state_enum(self, state: BrazilStatesEnum) -> None:
        self.state = state.state_symbol

    def __str__(self) -> str:
        if self.nickname:
            return f"({self.nickname}) {self.user}"
        return str(self.user)

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
            ),
        ]


class Vehicle(BaseModel):
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        help_text=_("Piloto relacionado ao Veículo"),
        related_query_name="vehicle_driver",
    )
    brand = models.CharField(max_length=30, help_text=_("Marca do veículo"))
    model = models.CharField(max_length=30, help_text=_("Modelo do veículo"))
    manufacture_year = models.IntegerField(help_text=_("Ano de Fabricação do veículo"))
    plate_number = models.CharField(
        max_length=8, unique=True, blank=True, null=True, help_text=_("Placa de identificação do veículo")
    )
    insured = models.BooleanField(default=False, help_text=_("Se o veículo possui seguro (Sim/Não)"))

    def __str__(self) -> str:
        return f"{self.brand} {self.model} - {self.plate_number}"

    class Meta:
        verbose_name = _("Veículo")
        verbose_name_plural = _("Veículos")

        constraints = [
            models.UniqueConstraint(
                fields=["plate_number"],
                name="unique_plate_number",
                condition=~Q(plate_number__isnull=True),
            )
        ]


class RaceHistory(BaseModel):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, help_text=_("Piloto relacionado ao histórico"))
    event = models.ForeignKey(
        "events.Event",
        on_delete=models.CASCADE,
        related_name=_("race_history"),
        help_text=_("Evento relacionado ao histórico"),
    )
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_query_name="vehicle_driver")
    position = models.IntegerField(help_text=_("Posição alcançada na corrida"))

    def __str__(self) -> str:
        return f"{self.driver} - {self.event}"

    class Meta:
        verbose_name = _("Histórico de Corrida")
        verbose_name_plural = _("Históricos de Corrida")


class LapTime(BaseModel):
    lap_number = models.IntegerField(help_text=_("Número da volta"))
    time = models.DurationField(help_text=_("Tempo da volta"))
    is_qualifying = models.BooleanField(default=False, help_text=_("Se a volta é de classificação (Sim/Não)"))
    is_valid = models.BooleanField(default=True, help_text=_("Se a volta é válida (Sim/Não)"))
    race_history = models.ForeignKey(
        RaceHistory,
        related_name="laps_time",
        on_delete=models.CASCADE,
        help_text=_("Histórico de corrida ao qual essa volta pertence"),
    )

    class Meta:
        verbose_name = _("Tempo de Volta")
        verbose_name_plural = _("Tempos de Volta")

    def __str__(self) -> str:
        if self.is_valid:
            return f"Volta {self.lap_number} - {self.time}"
        return _(f"Volta {self.lap_number} - {self.time} (Anulada)")
