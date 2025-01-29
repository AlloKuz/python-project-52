from django.urls import path
from .views import task_list, task_detail, task_create, task_edit, task_delete

urlpatterns = [
    path("", task_list, name="task_list"),
    path("<int:task_id>/", task_detail, name="task_detail"),
    path("create/", task_create, name="task_create"),
    path("<int:task_id>/edit/", task_edit, name="task_edit"),
    path("<int:task_id>/delete/", task_delete, name="task_delete"),
]
