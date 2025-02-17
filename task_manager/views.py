from django import views
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


class IndexView(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")


class LoginView(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, "registration/login.html")

    def post(self, request, *args, **kwargs):
        username = request.POST.get("loginUsername")
        password = request.POST.get("loginPassword")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, _("Вы залогинены"))
            return render(request, "index.html")
        else:
            messages.error(request, _("Пожалуйста, введите правильные имя пользователя и пароль. "
                                      "Оба поля могут быть чувствительны к регистру."))
            return render(request, "registration/login.html", context={"username": username})


class LogoutView(views.View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, _("Вы разлогинены"))
        return redirect(reverse("index"))


class UsersView(views.View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, "users.html", context={"users": users})