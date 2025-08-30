from datetime import datetime
from unittest.mock import patch

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Task
from users.models import CustomUser


class TaskTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            email="tester@sky.pro", full_name="Tester Testrov", post="Tester", is_director=True
        )

        self.task = Task.objects.create(
            title="Подготовить ТЗ",
            description="Подготовить ТЗ на установку АПС в АБК",
            owner=self.user,
            parent_task=None,
            is_parent=True,
            executor=self.user,
            deadline="2025-08-29 07:00:00",
            status="created",
            created_at="2025-01-09 14:00:00",
        )
        self.client.force_authenticate(user=self.user)

    def test_task_retrieve(self):
        """Тестирование просмотра задачи."""

        url = reverse("tasks:task-detail", args=(self.task.pk,))

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.task.title)

    def test_task_create(self):
        """Тестирование создания задачи."""

        url = reverse("tasks:task-create")
        data = {
            "title": "Обновить однолиненйные схемы",
            "owner": self.user,
            "is_parent": True,
            "executor": self.user,
            "deadline": "2025-09-09 17:00:00",
            "created_at": "2025-01-09 14:00:00",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.all().count(), 1)

    def test_task_update(self):
        """Тестирование изменения задачи."""

        url = reverse("tasks:task-edit", args=(self.task.pk,))
        data = {
            "description": "Подготовить ТЗ на установку АПС в Блоке 1А",
        }

        response = self.client.patch(url, data)
        self.assertEqual(data.get("description"), "Подготовить ТЗ на установку АПС в Блоке 1А")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_delete(self):
        """Тестирование удаления задачи."""

        url = reverse("tasks:task-delete", args=(self.task.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.all().count(), 0)

    def test_course_list(self):
        """Тестирование вывода списка курсов."""

        url = reverse("tasks:task-list")
        self.fixed_time = timezone.make_aware(datetime(2025, 1, 1, 12, 0))
        with patch("django.db.models.DateTimeField", auto_now_add=False):
            self.task = Task.objects.update(created_at=self.fixed_time)
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "title": "Подготовить ТЗ",
                    "description": "Подготовить ТЗ на установку АПС в АБК",
                    "owner": 1,
                    "parent_task": None,
                    "is_parent": True,
                    "executor": 1,
                    "deadline": "2025-08-29 07:00:00",
                    "status": "created",
                    "created_at": self.fixed_time.strftime("%Y-%m-%d %H:%M:%S"),
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
