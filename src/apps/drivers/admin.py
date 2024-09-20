from django.contrib import admin
from django.utils.html import format_html

from .models import Driver, Vehicle, RaceHistory, LapTime
from .forms import DriverForm, VehicleForm, RaceHistoryForm, LapTimeForm
from django.utils.translation import gettext_lazy as _


class VehicleAdmin(admin.TabularInline):
    model = Vehicle
    form = VehicleForm
    verbose_name = _("Dados do veículo")
    verbose_name_plural = _("Dados do veículo")
    extra = 0

    exclude = ("created_by", "updated_by")


class RaceHistoryAdmin(admin.TabularInline):
    model = RaceHistory
    form = RaceHistoryForm
    verbose_name = _("Histórico de corrida")
    verbose_name_plural = _("Históricos de corridas")
    extra = 0

    exclude = ("created_by", "updated_by")


@admin.register(LapTime)
class LapTimeAdmin(admin.ModelAdmin):
    form = LapTimeForm
    list_display = ("race_history", "lap_number", "time", "is_qualifying", "is_valid")
    search_fields = ("race_history__driver__user__user__username", "lap_number")
    list_filter = ("is_qualifying", "is_valid", "race_history__driver", "race_history__event")


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    inlines = (VehicleAdmin, RaceHistoryAdmin)
    form = DriverForm
    list_display = ("user", "nickname", "license_number", "category", "cba_number", "federation")
    search_fields = ("user__user__username", "nickname", "license_number", "cba_number")
    list_filter = ("category", "federation")
    list_select_related = True

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user__user")
