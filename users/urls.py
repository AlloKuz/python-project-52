from django.urls import path

from users import views


urlpatterns = [
    path('', views.UsersView.as_view(), name="users"),
    path('create/', views.UserFormView.as_view(), name="users_create"),
    path('<int:id>/update', views.UserUpdateView.as_view(),
         name="users_update"),
    path('<int:id>/delete', views.UserDeleteView.as_view(),
         name="users_delete"),
]