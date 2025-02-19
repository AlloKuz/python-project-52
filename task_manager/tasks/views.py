from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.views.generic import (ListView,
                                  CreateView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)
import logging

from task_manager.tasks.models import Task
from task_manager.tasks.filters import TasksFilter
from task_manager.users.mixins import LoginRequiredWithMessageMixin


logger = logging.getLogger(__name__)


class TaskListView(LoginRequiredWithMessageMixin, ListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filters"] = TasksFilter(self.request.GET,
                                         queryset=Task.objects.all(),
                                         request=self.request)
        return context


class TaskCreateView(LoginRequiredWithMessageMixin,
                     SuccessMessageMixin, CreateView):
    model = Task
    success_url = reverse_lazy("tasks")
    success_message = _("Task created")
    fields = ["name", "description", "executor", "status", "labels"]

    template_name = "form.html"

    extra_context = {
        "page_header": _("Create task"),
        "button_text": _("Create"),
    }

    def post(self, request, *args, **kwargs):
        data = super().post(request, *args, **kwargs)
        self.object.author = request.user
        self.object.save()
        return data


class TaskDetailView(LoginRequiredWithMessageMixin, DetailView):
    model = Task


class TaskUpdateView(LoginRequiredWithMessageMixin,
                     SuccessMessageMixin, UpdateView):
    model = Task
    fields = ["name", "description", "executor", "status", "labels"]
    success_url = reverse_lazy("tasks")
    success_message = _("Task updated")

    template_name = "form.html"

    extra_context = {
        "page_header": _("Edit task"),
        "button_text": _("Edit"),
    }


class TaskDeleteView(LoginRequiredWithMessageMixin,
                     SuccessMessageMixin, DeleteView):
    model = Task
    success_message = _("Task deleted")
    success_url = reverse_lazy("tasks")

    def get(self, request, pk, *args, **kwargs):
        data = super().get(request, pk, *args, **kwargs)
        if self.object.author_id != request.user.id:
            messages.error(request, _("Task can be deleted only by author"))
            return redirect(reverse_lazy('tasks'))
        return data

    def post(self, request, pk, *args, **kwargs):
        data = super().post(request, pk, *args, **kwargs)
        if self.object.author_id != request.user.id:
            messages.error(request, _("Task can be deleted only by author"))
            return redirect(reverse_lazy('tasks'))
        return data