from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import RegistrationView
from task_app.views import TaskCreateView, TaskListView, TaskRetrieveView, TaskDeleteView


urlpatterns = [
    path("admin/", admin.site.urls),
    
    # users
    path('api/register/', RegistrationView.as_view(), name="register"),
    path('api/login/', TokenObtainPairView.as_view(), name="login"),
    path('api/refresh/', TokenRefreshView.as_view(), name="refresh"),

    # tasks
    path('api/tasks/', TaskCreateView.as_view(), name="create-task"),
    path('api/tasks/', TaskListView.as_view(), name="list-task"),
    path('api/tasks/<int:id>/', TaskRetrieveView.as_view(), name="detials-task"),
    path('api/tasks/<int:id>/', TaskDeleteView.as_view(), name="delete-task")
]
