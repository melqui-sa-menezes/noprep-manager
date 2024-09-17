from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from apps.users_profiles.models import UserProfile
from apps.users_profiles.forms import UserProfileForm


class UserProfileInline(admin.TabularInline):
    fk_name = "user"
    model = UserProfile
    form = UserProfileForm
    can_delete = False
    verbose_name_plural = _("Dados complementares")
    verbose_name = _("Dados complementares")

    exclude = ("created_by", "updated_by", "hashed_tax_id", "masked_tax_id")


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "first_name", "last_name", "email", "password1", "password2"),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(CustomUserAdmin, self).get_form(request, obj, **kwargs)
        return form

    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
