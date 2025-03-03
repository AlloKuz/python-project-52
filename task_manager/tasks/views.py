import logging

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django_filters.views import FilterView

from task_manager.tasks.filters import TasksFilter
from task_manager.tasks.models import Task
from task_manager.users.mixins import LoginRequiredWithMessageMixin

logger = logging.getLogger(__name__)


class TaskListView(LoginRequiredWithMessageMixin, FilterView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'
    filterset_class = TasksFilter

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['request'] = self.request
        return kwargs

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filterset = getattr(self, 'filterset', None)
        if filterset:
            context['filter'] = filterset
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

    template_name = "confirm_deletion.html"

    extra_context = {
        "page_header": _("Delete task"),
        "deletion_msg": _("Are you sure you want to delete task")
    }

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author_id != request.user.id:
            messages.error(request, _("Task can be deleted only by author"))
            return redirect(reverse_lazy('tasks'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        data = super().get(request, *args, **kwargs)
        return data

    def post(self, request, *args, **kwargs):
        data = super().post(request, *args, **kwargs)
        if self.object.author_id != request.user.id:
            messages.error(request, _("Task can be deleted only by author"))
            return redirect(reverse_lazy('tasks'))
        return data
