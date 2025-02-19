from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin

from labels.models import Label
from labels.forms import LabelForm


class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        return render(request,
                      "labels/index.html",
                      {"labels": labels})


class CreateLabelView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = LabelForm()
        return render(request,
                      "labels/create.html",
                      {"form": form})

    def post(self, request, *args, **kwargs):
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, _("Метка успешно создана"))
            return redirect(reverse("labels"))
        return render(request,
                      "labels/create.html",
                      {"form": form})


class UpdateLabelView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        label = get_object_or_404(Label, id=id)
        form = LabelForm(instance=label)
        return render(request, "labels/update.html",
                      {"form": form, "label": label})

    def post(self, request, id, *args, **kwargs):
        label = get_object_or_404(Label, id=id)
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.info(request, _("Метка успешно изменена"))
            return redirect(reverse("labels"))
        return render(request, "labels/update.html",
                      {"form": form, "label": label})


class DeleteLabelView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        label = get_object_or_404(Label, id=id)
        return render(request,
                      "labels/delete.html",
                      {"label": label})

    def post(self, request, id, *args, **kwargs):
        label = get_object_or_404(Label, id=id)
        if label.task_set.exists():
            messages.error(request, _("Невозможно удалить метку, "
                                      "потому что она используется"))
        else:
            label.delete()
            messages.info(request, _("Метка успешно удалена"))
        return redirect(reverse("labels"))