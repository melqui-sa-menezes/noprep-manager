from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from common.helpers.enums.cities_states import BrazilStatesEnum
from .enums import CategoryEnum
from .forms import DriverAdminForm
from .models import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    form = DriverAdminForm
    list_display = (
        "driver_name",
        "city",
        "state_flag",
        "category_symbol",
        "cba_number"
    )
    list_filter = (
        "state",
        "category",
        "federation"
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            _("Informações Pessoais"),
            {
                "fields": (
                    "user_name",
                    "first_name",
                    "last_name",
                    "born_date",
                    "tax_id",
                    "city",
                    "state",
                    "email",
                    "license_number",
                )
            }
        ),
        (
            _("Dados da CBA"),
            {
                "fields": (
                    "cba_number",
                    "category",
                    "federation"
                )
            }
        ),
        (
            None,
            {
                "fields": (
                    "created_at",
                    "updated_at"
                )
            }
        )
    )


    @admin.display(description=_("Estado"))
    def state_flag(self, obj: Driver) -> str:
        state = BrazilStatesEnum.get(key=obj.state)
        if not state:
            return obj.user_full_name
        return format_html(
            '<img src="{}" width="16" height="auto"> {}',
            state.flag,
            state.state_symbol
        )

    @admin.display(description=_("Categoria"))
    def category_symbol(self, obj: Driver) -> str:
        return CategoryEnum(obj.category).name.replace("_", "-")


    @admin.display(description=_("Piloto"))
    def driver_name(self, obj: Driver) -> str:
        return obj.user_full_name
