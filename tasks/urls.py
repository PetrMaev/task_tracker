from django.urls import path

from tasks.apps import TasksConfig
from tasks.views import (
    TaskCreateAPIView,
    TaskDestroyAPIView,
    TaskListAPIView,
    TaskRetrieveAPIView,
    TaskUpdateAPIView,
    TaskUpdateAPIViewForExecutor,
)

app_name = TasksConfig.name

urlpatterns = [
    path("tasks/create/", TaskCreateAPIView.as_view(), name="task-create"),
    path("tasks/", TaskListAPIView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskRetrieveAPIView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/edit/", TaskUpdateAPIView.as_view(), name="task-edit"),
    path("tasks/<int:pk>/edit_executor/", TaskUpdateAPIViewForExecutor.as_view(), name="task-edit-executor"),
    path("tasks/<int:pk>/delete/", TaskDestroyAPIView.as_view(), name="task-delete"),
]
