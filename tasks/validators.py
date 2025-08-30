from django.utils import timezone
from rest_framework import serializers


class DeadlineValidator:
    __fields__ = ["deadline"]

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        deadline = dict(value).get(self.field)
        date_now = timezone.localtime()
        if deadline is not None:
            if deadline < date_now:
                raise serializers.ValidationError("Нельзя указывать прошедшую дату")
