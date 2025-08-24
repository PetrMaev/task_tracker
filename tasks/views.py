from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from tasks.models import Task
from tasks.serializers import TaskSerializer, TaskUpdateSerializer
from users.permissions import IsOwner, IsDirector, IsExecutor


class TaskCreateAPIView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated, IsDirector]

    def perform_create(self, serializer):
        task = serializer.save(owner=self.request.user)  # noqa: F841


class TaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsExecutor]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = []
    ordering_fields = []

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
