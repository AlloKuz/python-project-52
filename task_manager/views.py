from django import views
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.translation import gettext as _

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
            return render(request, "index.html")
        else:
            messages.error(request, _("Your username and password didn't match. Please try again."))
            return redirect(reverse("login"))
            # return render(request, "login.html", {"login_error": True})