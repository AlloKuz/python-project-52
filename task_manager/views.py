from django import views
from django.shortcuts import render


class IndexView(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")