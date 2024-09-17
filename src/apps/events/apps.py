from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EventsConfig(AppConfig):
    name = "apps.events"
    verbose_name = _("Eventos")

    def ready(self):
        import apps.events.models  # noqa
