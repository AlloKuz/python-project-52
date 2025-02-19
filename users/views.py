from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.deletion import ProtectedError
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from users.forms import UserForm
from users.mixins import UserOnlyEditThemselfPermissionMixin


class UserListView(ListView):
    model = User


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    success_message = _("User created")
    success_url = reverse_lazy("login")


class UserUpdateView(LoginRequiredMixin,
                     UserOnlyEditThemselfPermissionMixin,
                     SuccessMessageMixin,
                     UpdateView):
    model = User
    form_class = UserForm
    success_message = _("User updated")
    success_url = fail_url = reverse_lazy("users")
    template_name_suffix = "_update"

    raise_exception = False
    permission_denied_message = _("First you need to log in!")
    
    fail_message = _("You can't edit another user")


class UserDeleteView(LoginRequiredMixin,
                     UserOnlyEditThemselfPermissionMixin,
                     SuccessMessageMixin,
                     DeleteView):
    model = User
    success_message = _("User deleted")
    success_url = reverse_lazy("users")

    fail_message = _("You can't update another user")
    fail_url = reverse_lazy("users")
    
    def post(self, request, pk, *args, **kwargs):
        try:
            data = super().post(request, pk, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _("You can't delete user "
                                      "because it's in use"))
            return redirect(reverse("users"))
        return data