from django.urls import path

from task_manager.statuses.views import (StatusListView, StatusCreateView,
                                         StatusUpdateView, StatusDeleteView)

urlpatterns = [
    # path('', IndexView.as_view(), name="statuses"),
    path('', StatusListView.as_view(), name="statuses"),
    path('create/', StatusCreateView.as_view(), name="statuses_create"),
    path('<int:pk>/update/',
         StatusUpdateView.as_view(),
         name="statuses_update"),
    path('<int:pk>/delete/',
         StatusDeleteView.as_view(),
         name="statuses_delete"),
]