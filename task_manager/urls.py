from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from tasks.views import task_list, task_detail, task_create, task_edit, task_delete  # Импорт всех необходимых представлений

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),  # Включаем urls из приложения tasks
    path('', task_list, name='task_list'),  # Главная страница с задачами
    path('tasks/<int:pk>/', task_detail, name='task_detail'),  # Страница с подробностями задачи
    path('tasks/create/', task_create, name='task_create'),  # Страница для создания задачи
    path('tasks/<int:pk>/edit/', task_edit, name='task_edit'),  # Страница для редактирования задачи
    path('tasks/<int:pk>/delete/', task_delete, name='task_delete'),  # Страница для удаления задачи
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
