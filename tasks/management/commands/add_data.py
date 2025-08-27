from django.core.management import call_command
from django.core.management.base import BaseCommand

from tasks.models import Task


class Command(BaseCommand):
    help = "Load test data from fixture"

    def handle(self, *args, **kwargs):
        Task.objects.all().delete()

        call_command("loaddata", "tasks_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
