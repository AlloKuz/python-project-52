from django import views
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext as _


class IndexView(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, "task_manager/index.html")


class LoginView(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, "task_manager/login.html")

    def post(self, request, *args, **kwargs):
        username = request.POST.get("loginUsername")
        password = request.POST.get("loginPassword")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, _("Вы залогинены"))
            return redirect(reverse('index'))

        messages.error(request, _("Пожалуйста, введите правильные "
                                  "имя пользователя и пароль. Оба поля "
                                  "могут быть чувствительны к регистру."))
        return render(request,
                      "task_manager/login.html",
                      context={"username": username},
                      status=403)


class LogoutView(views.View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, _("Вы разлогинены"))
        return redirect(reverse("index"))