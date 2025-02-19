from django import views
from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.deletion import ProtectedError

from users.forms import UserCreateForm, UserUpdateForm


class UsersView(views.View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, "users/users.html",
                      context={"users": users})


class UserFormView(views.View):
    def get(self, request, *args, **kwargs):
        form = UserCreateForm()
        return render(request, "users/signup.html",
                      {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, _("Пользователь успешно зарегистрирован"))
            return redirect(reverse('login'))
        return render(request, "users/signup.html",
                      {"form": form})


class UserUpdateView(LoginRequiredMixin, views.View):

    def get(self, request, id, *args, **kwargs):
        if request.user.id != id:
            messages.error(request, _("У вас нет прав для изменения "
                                      "другого пользователя."))
            return redirect(reverse('users'))
        user = User.objects.get(id=id)
        form = UserUpdateForm(instance=user)
        if user:
            return render(request, "users/update.html",
                          {"form": form, "user_id": id})

    def post(self, request, id, *args, **kwargs):
        if request.user.id != id:
            messages.error(request, _("У вас нет прав для изменения "
                                      "другого пользователя."))
            return redirect(reverse('users'))
        user = User.objects.get(id=id)
        form = UserUpdateForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.info(request, _("Пользователь успешно изменен"))
            return redirect(reverse('index'))
        return render(request, "users/update.html",
                      {"form": form, "user_id": id})

    def handle_no_permission(self, *args, **kwargs):
        messages.error(self.request, _("Вы не авторизованы! "
                                       "Пожалуйста, выполните вход."))
        return super().handle_no_permission()


class UserDeleteView(LoginRequiredMixin, views.View):

    def get(self, request, id, *args, **kwargs):
        if request.user.id != id:
            messages.error(request, _("У вас нет прав для изменения "
                                      "другого пользователя."))
            return redirect(reverse('users'))
        user = User.objects.get(id=id)
        return render(request, "users/delete.html",
                      {"user": user})

    def post(self, request, id, *args, **kwargs):
        if request.user.id != id:
            messages.error(request, _("У вас нет прав для изменения "
                                      "другого пользователя."))
            return redirect(reverse('users'))
        try:
            user = User.objects.get(id=id)
            user.delete()
            messages.info(request, _("Пользователь успешно удален"))
        except ProtectedError:
            messages.error(request, _("Невозможно удалить пользователя, "
                                      "потому что он используется"))
        return redirect(reverse("users"))

    def handle_no_permission(self, *args, **kwargs):
        messages.error(self.request, _("Вы не авторизованы! "
                                       "Пожалуйста, выполните вход."))
        return super().handle_no_permission()