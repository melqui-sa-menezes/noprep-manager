from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DriversConfig(AppConfig):
    name = "apps.drivers"
    verbose_name = _("Pilotos")

    def ready(self):
        import apps.drivers.models  # noqa
