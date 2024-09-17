import datetime

from django import forms

from django.utils.translation import gettext_lazy as _

from apps.users_profiles.models import UserProfile
from common.helpers.enums.cities_states import BrazilStatesEnum
from common.helpers.utils.hash import hash_data


class UserProfileForm(forms.ModelForm):
    born_date = forms.DateField(
        label=_("Data de nascimento"),
        required=True,
        show_hidden_initial=True,
        widget=forms.DateInput(attrs={"type": "date"}),
        help_text=_("Data de nascimento do piloto"),
    )
    phone_number = forms.CharField(
        label=_("Telefone"),
        max_length=15,
        required=False,
        help_text=_("Telefone de contato"),
    )
    address = forms.CharField(
        label=_("Endereço"),
        max_length=255,
        required=False,
        help_text=_("Endereço de residência"),
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
    tax_id = forms.CharField(
        label=_("CPF"),
        max_length=14,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "000.000.000-00"}),
        help_text=_("Documento de indentificação (CPF)."),
    )

    class Meta:
        model = UserProfile
        fields = "__all__"
        exclude = ("created_by", "updated_by")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")

        if instance:
            this_year = datetime.date.today().year
            self.fields["born_date"].widget = forms.SelectDateWidget(
                attrs={"type": "date"}, years=range(this_year - 60, this_year - 13)
            )
            self.fields["tax_id"].initial = instance.masked_tax_id
            self.fields["tax_id"].widget.attrs["readonly"] = True

    def save(self, commit=True):
        try:
            if tax_id := self.cleaned_data.get("tax_id"):
                tax_id = str(tax_id).replace(".", "").replace("-", "")
                self.instance.hashed_tax_id = hash_data(tax_id)
                self.instance.masked_tax_id = f"{tax_id[:3]}.***.***-{tax_id[-2:]}"
        except Exception as error:
            self.add_error(None, error)
            commit = False

        finally:
            return super().save(commit)
