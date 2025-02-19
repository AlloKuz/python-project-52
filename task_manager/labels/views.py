from django.shortcuts import reverse, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.labels.models import Label
from task_manager.users.mixins import LoginRequiredWithMessageMixin


class LabelListView(LoginRequiredWithMessageMixin, ListView):
    model = Label


class LabelCreateView(LoginRequiredWithMessageMixin,
                      SuccessMessageMixin, CreateView):
    model = Label
    fields = ["name"]
    success_url = reverse_lazy("labels")
    success_message = _("Label created")

    template_name = "form.html"

    extra_context = {
        "page_header": _("Create label"),
        "button_text": _("Create"),
    }


class LabelUpdateView(LoginRequiredWithMessageMixin,
                      SuccessMessageMixin, UpdateView):
    model = Label
    fields = ["name"]
    success_url = reverse_lazy("labels")
    success_message = _("Label updated")

    template_name = "form.html"

    extra_context = {
        "page_header": _("Edit label"),
        "button_text": _("Edit"),
    }


class LabelDeleteView(LoginRequiredWithMessageMixin,
                      SuccessMessageMixin, DeleteView):
    model = Label
    success_url = reverse_lazy("labels")
    success_message = _("Label deleted")

    template_name = "confirm_deletion.html"

    extra_context = {
        "page_header": _("Delete label"),
        "deletion_msg": _("Are you sure you want to delete label")
    }

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        if label.task_set.exists():
            messages.error(request, _("Unable to delete label"))
            return redirect(reverse("labels"))
        return super().post(request, *args, **kwargs)