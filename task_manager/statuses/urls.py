from django.urls import path

from statuses.views import IndexView, StatusCreateView

urlpatterns = [
    path('', IndexView.as_view(), name="statuses"),
    path('create/', StatusCreateView.as_view(), name="statuses_create"),
    ]