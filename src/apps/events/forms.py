from django import forms
from .models import Subscription
from django.utils.translation import gettext_lazy as _


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ["vehicle"]

    def __init__(self, *args, **kwargs):
        driver = kwargs.pop("driver")
        super().__init__(*args, **kwargs)
        self.fields["vehicle"].queryset = driver.vehicle_set.all()

    def clean(self):
        cleaned_data = super().clean()
        vehicle = cleaned_data.get("vehicle")
        driver = self.instance.driver

        if vehicle and vehicle.driver != driver:
            self.add_error("vehicle", _("O veículo selecionado não pertence ao piloto."))
