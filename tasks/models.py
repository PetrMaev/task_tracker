from django.core.exceptions import ValidationError
from django.db import models

from users.models import CustomUser


class Task(models.Model):
    CREATED = "created"
    WORK = "work"
    COMPLETED = "completed"

    STATUS_CHOICES = [
        (CREATED, "Создана"),
        (WORK, "В работе"),
        (COMPLETED, "Завершена"),
    ]

    title = models.CharField(
        max_length=255, verbose_name="Наименование задачи", help_text="Укажите наименование задачи"
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание задачи", help_text="Укажите описание задачи"
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Автор задачи",
    )
    parent_task = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Родительская задача",
    )
    is_parent = models.BooleanField(default=False, verbose_name="Родительская задача")
    executor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Исполнитель",
    )
    deadline = models.DateTimeField(verbose_name="Срок исполнения задачи")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=CREATED, verbose_name="Статус задачи")
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # В родительские задачи могут попадать только задачи с признаком родительской задачи
        if self.parent_task and not self.parent_task.is_parent:
            raise ValidationError(
                "В родительские задачи могут попадать только задачи с признаком родительской задачи."
            )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
