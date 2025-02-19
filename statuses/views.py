from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from statuses.models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    fields = ["name"]
    success_url = reverse_lazy("statuses")
    success_message = _("Status created")


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    fields = ["name"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("statuses")
    success_message = _("Status updated")


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    success_url = reverse_lazy("statuses")
    success_message = _("Status deleted")