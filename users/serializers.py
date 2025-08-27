from rest_framework import serializers

from tasks.serializers import TaskSerializer
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    tasks_count = serializers.SerializerMethodField()
    tasks_active_count = serializers.SerializerMethodField()
    tasks = TaskSerializer(many=True, read_only=True)
    ordering_fields = ["tasks_count", "tasks_active_count"]

    def get_tasks_count(self, user):
        return user.tasks.count()

    def get_tasks_active_count(self, user):
        return user.tasks.filter(status="work").count()

    class Meta:
        model = CustomUser
        fields = ["id", "full_name", "email", "post", "tasks_count", "tasks_active_count", "tasks"]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "full_name", "post", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class FreeUserSerializer(serializers.ModelSerializer):
    task_title = serializers.ReadOnlyField()
    deadline = serializers.DateTimeField()
    employee = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        fields = ["task_title", "deadline", "employee"]
