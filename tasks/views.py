from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views import View
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

from tasks.forms import TaskForm
from tasks.models import Task
from tasks.filters import TasksFilter


logger = logging.getLogger(__name__)


class TasksView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        filters = TasksFilter(request.GET,
                              queryset=Task.objects.all(),
                              request=request)
        return render(request, "tasks/index.html",
                      {"filters": filters})


class TasksCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, "tasks/create.html",
                      context={"form": form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            messages.info(request, _("Задача успешно создана"))
            return redirect(reverse("tasks"))
        return render(request, "tasks/create.html",
                      {"form": form}, status=300)
            

class TasksShowView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        task = get_object_or_404(Task, id=id)
        return render(request, "tasks/show.html",
                      {"task": task})


class TasksUpdateView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        task = get_object_or_404(Task, id=id)
        form = TaskForm(instance=task)
        return render(request, "tasks/update.html",
                      {"task": task, "form": form})

    def post(self, request, id, *args, **kwargs):
        task = get_object_or_404(Task, id=id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.info(request, _("Задача успешно изменена"))
            return redirect(reverse("tasks"))
        return render(request, "tasks/update.html",
                      {"form": form, "task": task})


class TasksDeleteView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        task = get_object_or_404(Task, id=id)
        if task.author_id == request.user.id:
            return render(request, "tasks/delete.html",
                          {"task": task})
        messages.error(request, _("Задачу может удалить только ее автор"))
        return redirect(reverse("tasks"))

    def post(self, request, id, *args, **kwargs):
        task = get_object_or_404(Task, id=id)
        if task.author_id == request.user.id:
            task.delete()
            messages.info(request, _("Задача успешно удалена"))
        return redirect(reverse("tasks"))