from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages

from task_manager.statuses.models import Status
from task_manager.users.mixins import LoginRequiredWithMessageMixin


class StatusListView(LoginRequiredWithMessageMixin, ListView):
    model = Status


class StatusCreateView(LoginRequiredWithMessageMixin,
                       SuccessMessageMixin, CreateView):
    model = Status
    fields = ["name"]
    success_url = reverse_lazy("statuses")
    success_message = _("Status created")

    template_name = "form.html"

    extra_context = {
        "page_header": _("Create status"),
        "button_text": _("Create"),
    }


class StatusUpdateView(LoginRequiredWithMessageMixin,
                       SuccessMessageMixin, UpdateView):
    model = Status
    fields = ["name"]
    success_url = reverse_lazy("statuses")
    success_message = _("Status updated")

    template_name = "form.html"

    extra_context = {
        "page_header": _("Edit status"),
        "button_text": _("Edit"),
    }


class StatusDeleteView(LoginRequiredWithMessageMixin,
                       SuccessMessageMixin, DeleteView):
    model = Status
    success_url = reverse_lazy("statuses")
    success_message = _("Status deleted")

    template_name = "confirm_deletion.html"

    extra_context = {
        "page_header": _("Delete status"),
        "deletion_msg": _("Are you sure you want to delete status")
    }

    def post(self, request, *args, **kwargs):
        status = self.get_object()
        if status.task_set.exists():
            messages.error(request, _("Unable to delete status"))
            return redirect(reverse_lazy("statuses"))
        data = super().post(request, *args, **kwargs)
        return data