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


class UserListView(ListView):
    model = User


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    success_message = _("User created")
    success_url = reverse_lazy("login")


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    success_message = _("User updated")
    success_url = reverse_lazy("users")
    template_name_suffix = "_update"

    def get(self, request, pk, *args, **kwargs):
        if request.user.id != pk:
            messages.error(request, _("You can't edit another user"))
            return redirect(reverse_lazy('users'))
        return super().get(request, pk, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_message = _("User deleted")
    success_url = reverse_lazy("users")

    def get(self, request, pk, *args, **kwargs):
        if request.user.id != pk:
            messages.error(request, _("You can't update another user"))
            return redirect(reverse_lazy('users'))
        return super().get(request, pk, *args, **kwargs)
    
    def post(self, request, pk, *args, **kwargs):
        try:
            data = super().post(request, pk, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _("You can't delete user "
                                      "because it's in use"))
            return redirect(reverse("users"))
        return data