from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser


class CustomUserTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            email="tester@sky.pro", full_name="Tester Testrov", post="Tester", is_director=True
        )
        self.client.force_authenticate(user=self.user)

    def test_user_retrieve(self):
        """Тестирование просмотра пользователя."""

        url = reverse("users:user-detail", args=(self.user.pk,))

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), self.user.email)

    def test_user_create(self):
        """Тестирование создания пользователя."""

        url = reverse("users:user-register")
        data = {
            "email": "tester2@sky.pro",
            "password": "123qwe",
            "full_name": "Tester Testerovich",
            "post": "Tester junior",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.all().count(), 2)

    def test_user_update(self):
        """Тестирование изменения пользователя."""

        url = reverse("users:user-edit", args=(self.user.pk,))
        data = {"email": "tester2222@sky.pro"}
        response = self.client.patch(url, data)

        self.assertEqual(data.get("email"), "tester2222@sky.pro")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_delete(self):
        """Тестирование удаления пользователя."""

        url = reverse("users:user-delete", args=(self.user.pk,))

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.all().count(), 0)

    def test_user_list(self):
        """Тестирование вывода списка пользователей."""

        url = reverse("users:user-list")

        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": 9,
                "full_name": "Tester Testrov",
                "email": "tester@sky.pro",
                "post": "Tester",
                "tasks_count": 0,
                "tasks_active_count": 0,
                "tasks": [],
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
