from django.contrib import admin
from django.urls import path, include  # Импортируем include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", include("tasks.urls")),  # Подключаем маршруты приложения tasks
]
