from django.contrib import admin
from apps.drivers.models import Driver, Vehicle, RaceHistory, LapTime
from apps.drivers.forms import DriverForm, VehicleForm, RaceHistoryForm, LapTimeForm


class DriverAdmin(admin.ModelAdmin):
    form = DriverForm
    list_display = ("user", "nickname", "license_number", "category", "cba_number", "federation")
    search_fields = ("user__user__username", "nickname", "license_number", "cba_number")
    list_filter = ("category", "federation")


class VehicleAdmin(admin.ModelAdmin):
    form = VehicleForm
    list_display = ("brand", "model", "manufacture_year", "plate_number", "driver")
    search_fields = ("driver__user__user__username", "plate_number", "chassis_number")
    list_filter = ("brand", "model", "manufacture_year", "insured")


class RaceHistoryAdmin(admin.ModelAdmin):
    form = RaceHistoryForm
    list_display = ("driver", "event", "position")
    search_fields = ("driver__user__user__username", "event__name")
    list_filter = ("event",)


class LapTimeAdmin(admin.ModelAdmin):
    form = LapTimeForm
    list_display = ("race_history", "lap_number", "time", "is_qualifying", "is_valid")
    search_fields = ("race_history__driver__user__user__username", "lap_number")
    list_filter = ("is_qualifying", "is_valid")


admin.site.register(Driver, DriverAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(RaceHistory, RaceHistoryAdmin)
admin.site.register(LapTime, LapTimeAdmin)
