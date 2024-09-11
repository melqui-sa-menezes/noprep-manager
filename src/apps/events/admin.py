from django.contrib import admin
from .models import EventType, Event

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_per_page = 20

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'organizer', 'event_type', 'fee')
    search_fields = ('name', 'organizer__name', 'address')
    list_filter = ('date', 'event_type', 'organizer')
    ordering = ('date', 'name')
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': ('name', 'date', 'starts_at', 'ends_at', 'address', 'fee', 'organizer', 'event_type', 'regulation')
        }),
    )
    autocomplete_fields = ['organizer', 'event_type']
    date_hierarchy = 'date'

    def starts_at(self, obj):
        if obj:
            return obj.starts_at
    starts_at.short_description = 'Horário de Início'

    def ends_at(self, obj):
        if obj:
            return obj.ends_at
    ends_at.short_description = 'Horário de Término'
