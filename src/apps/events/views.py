from django.urls import reverse
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Subscription, Event
from .forms import SubscriptionForm
from src.apps.drivers.models import Driver


class EventSubscriptionView(LoginRequiredMixin, CreateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = "events/subscribe.html"

    def dispatch(self, request, *args, **kwargs):
        self.event = Event.objects.get(pk=self.kwargs["event_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            driver = self.request.user.userprofile.driver
        except Driver.DoesNotExist:
            driver = None
        kwargs["driver"] = driver
        return kwargs

    def form_valid(self, form):
        form.instance.driver = self.request.user.userprofile.driver
        form.instance.event = self.event
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("event_detail", kwargs={"pk": self.event.pk})
