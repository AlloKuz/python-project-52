from django.shortcuts import render, reverse, redirect
from django.views import View
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from tasks.forms import TaskForm
from tasks.models import Task


class TasksView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        return render(request, "tasks/index.html",
                      {"tasks": tasks})


class TasksCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, "tasks/create.html",
                      context={"form": form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        form.author = request.user
        if form.is_valid():
            form.save()
            messages.info(request, _("Задача успешно добавлена"))
            return redirect(reverse("tasks"))
        messages.info(request, _("Ошибка добавления задачи"))
        return render(request, "tasks/create.html",
                      {"form": form})


class TasksShowView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        task = Task.objects.get(id=id)
        return render(request, "tasks/show.html",
                      {"task": task})


class TasksUpdateView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        task = Task.objects.get(id=id)
        form = TaskForm(instance=task)
        return render(request, "tasks/update.html",
                      {"task": task, "form": form})

    def post(self, request, id, *args, **kwargs):
        task = Task.objects.get(id=id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.info(request, _("Задача успешно изменена"))
            return redirect(reverse("tasks"))
        messages.error(request, _("Ошибка изменения задачи"))
        return render(request, "tasks/update.html",
                      {"form": form, "task": task})


class TasksDeleteView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        task = Task.objects.get(id=id)
        if task.author_id == request.user.id:
            return render(request, "tasks/delete.html",
                          {"task": task})
        messages.error(request, _("Задачу может удалить только ее автор"))
        return redirect(reverse("tasks"))

    def post(self, request, id, *args, **kwargs):
        task = Task.objects.get(id=id)
        if task.author_id == request.user.id:
            task.delete()
            messages.info(request, _("Задача успешно удалена"))
        return redirect(reverse("tasks"))