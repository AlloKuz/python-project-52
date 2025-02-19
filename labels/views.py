from django.shortcuts import reverse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

from labels.models import Label
from users.mixins import LoginRequiredWithMessageMixin


class LabelListView(LoginRequiredWithMessageMixin, ListView):
    model = Label


class LabelCreateView(LoginRequiredWithMessageMixin,
                      SuccessMessageMixin, CreateView):
    model = Label
    fields = ["name"]
    success_url = reverse_lazy("labels")
    success_message = _("Label created")


class LabelUpdateView(LoginRequiredWithMessageMixin,
                      SuccessMessageMixin, UpdateView):
    model = Label
    fields = ["name"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("labels")
    success_message = _("Label updated")


class LabelDeleteView(LoginRequiredWithMessageMixin,
                      SuccessMessageMixin, DeleteView):
    model = Label
    success_url = reverse_lazy("labels")
    success_message = _("Label deleted")

    def post(self, request, pk, *args, **kwargs):
        label = get_object_or_404(Label, pk=pk)
        if label.task_set.exists():
            messages.error(request, _("Deletion error"))
            return redirect(reverse("labels"))
        return super().post(request, *args, **kwargs)