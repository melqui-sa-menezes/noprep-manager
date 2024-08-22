from django import forms
from django.contrib.auth.models import User
from django.db.models import DateField
from django.forms import DateInput

from apps.drivers.enums import CategoryEnum, FederationEnum
from django.utils.translation import gettext_lazy as _

from apps.drivers.models import Driver

__all__ = ["DriverAdminForm"]

from common.helpers.enums.cities_states import BrazilStatesEnum


class DriverAdminForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        label=_("Usuário"),
        queryset=User.objects.all(),
        required=False,
        help_text=_("Usuário associado ao piloto"),
    )
    user_name = forms.CharField(
        label=_("Nome de usuário"),
        max_length=150,
        required=True,
        help_text=_("Nome de usuário para acesso ao sistema. Ex: joao.silva"),
    )
    first_name = forms.CharField(
        label=_("Nome"),
        max_length=30,
        required=True,
        help_text=_("Nome do piloto")
    )
    last_name = forms.CharField(
        label=_("Sobrenome"),
        max_length=150,
        required=True,
        help_text=_("Sobrenome do piloto"),
    )
    # TODO: investigar porque nao apresenta a data salva no admin
    born_date = forms.DateField(
        label=_("Data de nascimento"),
        required=True,
        show_hidden_initial=True,
        widget=forms.DateInput(attrs={"type": "date", "format": "%Y-%m-%d"}),
        help_text=_("Data de nascimento do piloto"),
    )
    city = forms.CharField(
        label=_("Cidade"),
        max_length=30,
        required=True,
        help_text=_("Cidade onde reside"),
    )
    state = forms.ChoiceField(
        label=_("Estado"),
        choices=sorted(BrazilStatesEnum.get_database_choices(by_name=True)),
        widget=forms.Select,
        required=True,
        help_text=_("Estado onde reside"),
    )
    email = forms.EmailField(
        label=_("E-mail"),
        max_length=254,
        widget=forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
        required=True
    )
    tax_id = forms.CharField(
        label=_("CPF"),
        max_length=11,
        required=True,
        help_text=_("Documento de indentificação (CPF)"),
    )
    license_number = forms.CharField(
        label=_("CNH"),
        max_length=50,
        required=False,
        help_text=_("Número da carteira de habilitação"),
    )
    cba_number = forms.CharField(
        label=_("Número CBA"),
        max_length=12,
        required=False,
        help_text=_("Número de registro CBA"),
    )
    category = forms.ChoiceField(
        label=_("Categoria"),
        choices=sorted(CategoryEnum.get_database_choices()),
        required=False,
        help_text=_("Categoria da licença"),
    )
    federation = forms.ChoiceField(
        label=_("Federação"),
        choices=sorted(FederationEnum.get_database_choices()),
        required=False,
        help_text=_("Federação de origem do piloto"),
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")

        if instance:
            user = instance.user
            self.fields["user_name"].initial = user.username
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["state"].initial = BrazilStatesEnum.get(key=instance.state).state_name
            self.fields["email"].initial = user.email


    def save(self, commit=True):
        new_user = User.objects.create_user(
            username=self.data["user_name"],
            first_name=self.data["first_name"],
            last_name=self.data["last_name"],
            email=self.data["email"]
        )
        new_user.save()
        self.instance.user = new_user
        return super().save(commit=commit)

    class Meta:
        fields = "__all__"
        model = Driver

