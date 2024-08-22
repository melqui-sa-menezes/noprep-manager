from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path

# Register Routes
urlpatterns = []

# Django Admin
admin.site.site_header = "Project Flow Manager"
admin.site.site_title = "Project Flow Manager"
admin.site.index_title = "Welcome to Project Flow Manager"

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    prefix_default_language=False,
)
