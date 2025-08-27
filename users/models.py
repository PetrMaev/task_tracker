from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(
        max_length=255, verbose_name="Фамилия, имя, отчество", help_text="Укажите фамилию, имя и отчество"
    )
    post = models.CharField(max_length=250, verbose_name="Должность", help_text="Укажите должность")
    is_director = models.BooleanField(default=False, verbose_name="Является ли пользователь руководителем")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
