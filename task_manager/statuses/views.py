from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext as _

from statuses.models import Status
from statuses.forms import StatusForm


class IndexView(View):

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(request, "statuses/index.html",
                      context={"statuses": statuses})


class StatusCreateView(View):

    def get(self, request, *args, **kwargs):
        form = StatusForm()
        return render(request, "statuses/create.html",
                      {"form": form})

    def post(self, request, *args, **kwargs):
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, _("Статус успешно создан"))
            return redirect(reverse("statuses"))
        messages.error(request, _("Неправильное имя статуса"))
        return render(request, "statuses/create.html",
                      {"form": form})