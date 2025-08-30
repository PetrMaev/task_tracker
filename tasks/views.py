from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from tasks.filters import TaskFilter
from tasks.models import Task
from tasks.paginators import CustomPagination
from tasks.serializers import TaskSerializer, TaskUpdateSerializer
from users.permissions import IsDirector, IsExecutor, IsOwner


class TaskCreateAPIView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsDirector]

    def perform_create(self, serializer):
        task = serializer.save(owner=self.request.user)  # noqa: F841


class TaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsExecutor]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        if queryset.filter(owner=self.request.user):
            return queryset
        else:
            return queryset.filter(executor=self.request.user)


class TaskRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsExecutor]


class TaskUpdateAPIView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class TaskUpdateAPIViewForExecutor(generics.UpdateAPIView):
    serializer_class = TaskUpdateSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsExecutor]


class TaskDestroyAPIView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
