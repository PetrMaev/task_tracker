from rest_framework import serializers

from tasks.models import Task
from tasks.validators import DeadlineValidator


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"
        validators = [DeadlineValidator(field="deadline")]


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["title", "description", "owner", "parent_task", "is_parent", "executor", "deadline", "status",
                  "created_at"]
        extra_kwargs = {
            "title": {"read_only": True},
            "description": {"read_only": True},
            "owner": {"read_only": True},
            "parent_task": {"read_only": True},
            "is_parent": {"read_only": True},
            "executor": {"read_only": True},
            "deadline": {"read_only": True},
            "created_at": {"read_only": True},
        }
