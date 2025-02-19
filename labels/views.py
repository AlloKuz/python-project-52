from django.shortcuts import reverse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from labels.models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    fields = ["name"]
    success_url = reverse_lazy("labels")
    success_message = _("Label created")


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    fields = ["name"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("labels")
    success_message = _("Label updated")


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    success_url = reverse_lazy("labels")
    success_message = _("Label deleted")

    def post(self, request, pk, *args, **kwargs):
        label = get_object_or_404(Label, pk=pk)
        if label.task_set.exists():
            messages.error(request, _("Can't delete label because it's in use"))
            return redirect(reverse("labels"))
        return super().post(request, *args, **kwargs)