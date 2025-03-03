from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.users.forms import UserForm, UserUpdateForm
from task_manager.users.mixins import (
    LoginRequiredWithMessageMixin,
    UserOnlyEditThemselfPermissionMixin,
)
from task_manager.users.models import User


class UserListView(ListView):
    model = User


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    success_message = _("User created")
    success_url = reverse_lazy("login")

    template_name = "form.html"

    extra_context = {
        "page_header": _("Create user"),
        "button_text": _("Sign me up"),
    }


class UserUpdateView(LoginRequiredWithMessageMixin,
                     UserOnlyEditThemselfPermissionMixin,
                     SuccessMessageMixin,
                     UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = fail_url = reverse_lazy("users")

    success_message = _("User updated")
    no_auth_message = _("First you need to log in!")
    fail_message = _("You are not allowed to edit another user")

    template_name = "form.html"

    extra_context = {
        "page_header": _("Edit user"),
        "button_text": _("Edit"),
    }


class UserDeleteView(LoginRequiredWithMessageMixin,
                     UserOnlyEditThemselfPermissionMixin,
                     SuccessMessageMixin,
                     DeleteView):
    model = User
    success_url = reverse_lazy("users")
    fail_url = reverse_lazy("users")
    template_name = "confirm_deletion.html"

    success_message = _("User deleted")
    fail_message = _("You are not allowed to delete another user")
    no_auth_message = _("First you need to log in!")

    extra_context = {
        "page_header": _("Delete user"),
        "deletion_msg": _("Are you sure you want to delete user")
    }

    def post(self, request, *args, **kwargs):
        try:
            data = super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _("Unable to delete user"))
            return redirect(reverse("users"))
        return data
