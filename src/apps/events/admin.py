from django.contrib import admin
from django.core.mail import EmailMessage
from django.utils.html import format_html
from simple_settings import settings

from .models import EventType, Event, Subscription


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")
    ordering = ("name",)
    list_per_page = 20


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "event_type", "date", "fee", "view_subscriptions", "count_subscriptions")
    search_fields = ("name", "organizer__name", "address")
    list_filter = ("date", "event_type", "organizer")
    ordering = ("date", "name")
    list_per_page = 20
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "date",
                    "starts_at",
                    "ends_at",
                    "address",
                    "fee",
                    "organizer",
                    "event_type",
                    "regulation",
                )
            },
        ),
    )
    autocomplete_fields = ["organizer", "event_type"]
    date_hierarchy = "date"

    def starts_at(self, obj):
        if obj:
            return obj.starts_at

    starts_at.short_description = "Horário de Início"

    def ends_at(self, obj):
        if obj:
            return obj.ends_at

    ends_at.short_description = "Horário de Término"

    @admin.display(description="Pilotos")
    def view_subscriptions(self, obj):
        return format_html(
            "<a href='{}'>Ver inscrições</a>",
            f"/admin/events/subscription/?event__id__exact={obj.id}",
        )

    @admin.display(description="Inscritos")
    def count_subscriptions(self, obj):
        return Subscription.objects.filter(event__id=obj.id).count()


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("driver_nickname", "subscription_date", "event", "status")
    list_filter = ("event", "event__date")
    ordering = ("-subscription_date",)
    list_per_page = 20
    fieldsets = (
        (
            None,
            {"fields": ("event", "driver", "status", "created_at")},
        ),
    )
    autocomplete_fields = ["event"]
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
    actions = ["send_confirmation_email"]

    @admin.display(description="Piloto")
    def driver_nickname(self, obj):
        return format_html(
            "<a href='/admin/drivers/driver/{}/change/'>{}</a>",
            obj.driver.id,
            obj.driver.nickname,
        )

    def send_confirmation_email(self, request, queryset):
        subscription_data = [(subscription.driver.user.user.email, subscription.event) for subscription in queryset]
        email_recipients = [email for email, _ in subscription_data]
        event = [event for _, event in subscription_data][0]

        if email_recipients:
            email = EmailMessage(
                subject="Confirmação de Inscrição",
                body=(
                    f"Você foi inscrito com sucesso para o evento {event.name.upper()}, "
                    f"que será realizado no dia {event.date.strftime('%d/%m/%Y')}.\n\n"
                ),
                from_email=settings.EMAIL_HOST_USER,
                to=email_recipients,
            )
            email.send()
            self.message_user(
                request,
                f"E-mail de confirmação enviado para {', '.join(email_recipients)}",
            )
        else:
            self.message_user(
                request,
                "Nenhum e-mail de inscrição encontrado",
            )

    send_confirmation_email.short_description = "Enviar e-mail de confirmação"
