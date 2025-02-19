from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.deletion import ProtectedError
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import SetPasswordForm

from users.forms import UserCreateForm


class UserListView(ListView):
    model = User


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateForm
    success_message = _("Пользователь успешно зарегистрирован")
    success_url = reverse_lazy("login")


class UserUpdateView(LoginRequiredMixin, UpdateView, SetPasswordForm):
    model = User
    # form_class = UserUpdateForm
    fields = ["first_name", "last_name", "username"]
    success_message = _("Пользователь успешно изменен")
    success_url = reverse_lazy("users")
    template_name_suffix = "_update"

    def get(self, request, pk, *args, **kwargs):
        if request.user.id != pk:
            messages.error(request, _("У вас нет прав для изменения "
                                      "другого пользователя."))
            return redirect(reverse_lazy('users'))
        return super().get(request, pk, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_message = _("Пользователь успешно удален")
    success_url = reverse_lazy("users")

    def get(self, request, pk, *args, **kwargs):
        if request.user.id != pk:
            messages.error(request, _("У вас нет прав для изменения "
                                      "другого пользователя."))
            return redirect(reverse_lazy('users'))
        return super().get(request, pk, *args, **kwargs)
    
    def post(self, request, pk, *args, **kwargs):
        try:
            data = super().post(request, pk, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _("Невозможно удалить пользователя, "
                                      "потому что он используется"))
            return redirect(reverse("users"))
        return data