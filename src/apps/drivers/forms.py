from django import forms
from django.utils.translation import gettext_lazy as _
from apps.drivers.models import Driver, Vehicle, RaceHistory, LapTime
from apps.events.models import Event
from apps.user_profiles.models import UserProfile
from apps.drivers.enums import CategoryEnum, FederationEnum


class DriverForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=UserProfile.objects.all(),
        label=_("Usuário"),
        help_text=_("Usuário associado ao piloto"),
    )
    nickname = forms.CharField(max_length=32, required=False, label=_("Apelido"), help_text=_("Apelido do piloto"))
    license_number = forms.CharField(
        max_length=9,
        required=False,
        label=_("Número da carteira de habilitação"),
        help_text=_("Número da carteira de habilitação"),
    )
    category = forms.ChoiceField(
        choices=CategoryEnum.get_database_choices(),
        label=_("Categoria da licença"),
        help_text=_("Categoria da licença"),
    )
    cba_number = forms.CharField(
        max_length=12, required=False, label=_("Número de registro CBA"), help_text=_("Número de registro CBA")
    )
    federation = forms.ChoiceField(
        choices=FederationEnum.get_database_choices(),
        label=_("Federação"),
        help_text=_("Federação de origem do piloto"),
    )

    class Meta:
        model = Driver
        fields = ["user", "nickname", "license_number", "category", "cba_number", "federation"]


# Form para o modelo Vehicle
class VehicleForm(forms.ModelForm):
    driver = forms.ModelChoiceField(
        queryset=Driver.objects.all(), label=_("Piloto"), help_text=_("Piloto relacionado ao veículo")
    )
    brand = forms.CharField(max_length=30, label=_("Marca"), help_text=_("Marca do veículo"))
    model = forms.CharField(max_length=30, label=_("Modelo"), help_text=_("Modelo do veículo"))
    manufacture_year = forms.IntegerField(label=_("Ano de Fabricação"), help_text=_("Ano de Fabricação do veículo"))
    plate_number = forms.CharField(max_length=8, label=_("Placa"), help_text=_("Placa de identificação do veículo"))
    insured = forms.BooleanField(required=False, label=_("Seguro"), help_text=_("Se o veículo possui seguro (Sim/Não)"))

    class Meta:
        model = Vehicle
        fields = [
            "driver",
            "brand",
            "model",
            "manufacture_year",
            "plate_number",
            "insured",
        ]


# Form para o modelo RaceHistory
class RaceHistoryForm(forms.ModelForm):
    driver = forms.ModelChoiceField(
        queryset=Driver.objects.all(), label=_("Piloto"), help_text=_("Piloto relacionado ao histórico")
    )
    event = forms.ModelChoiceField(
        queryset=Event.objects.all(), label=_("Evento"), help_text=_("Evento relacionado ao histórico")
    )
    position = forms.IntegerField(label=_("Posição"), help_text=_("Posição alcançada na corrida"))

    class Meta:
        model = RaceHistory
        fields = ["driver", "event", "position"]


# Form para o modelo LapTime
class LapTimeForm(forms.ModelForm):
    lap_number = forms.IntegerField(label=_("Número da volta"), help_text=_("Número da volta"))
    time = forms.DurationField(label=_("Tempo da volta"), help_text=_("Tempo da volta"))
    is_qualifying = forms.BooleanField(
        required=False, label=_("Classificação"), help_text=_("Se a volta é de classificação (Sim/Não)")
    )
    is_valid = forms.BooleanField(required=False, label=_("Volta Válida"), help_text=_("Se a volta é válida (Sim/Não)"))
    race_history = forms.ModelChoiceField(
        queryset=RaceHistory.objects.all(),
        label=_("Histórico de Corrida"),
        help_text=_("Histórico de corrida ao qual essa volta pertence"),
    )

    class Meta:
        model = LapTime
        fields = ["lap_number", "time", "is_qualifying", "is_valid", "race_history"]
