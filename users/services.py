from django.db.models import Count, Q

from tasks.models import Task
from users.models import CustomUser


def get_free_employees():
    """Возвращает список словарей с наименованием задачи, сроком и наименее занятым сотрудником."""
    employees = CustomUser.objects.annotate(tasks_active_count=Count("tasks", filter=Q(tasks__status="work")))
    critical_tasks = Task.objects.filter(
        status=Task.CREATED,
        is_parent=True,
    ).distinct()

    min_tasks_count = min(emp.tasks_active_count for emp in employees)

    free_employees = employees.filter(
        Q(tasks_active_count=min_tasks_count) | Q(tasks_active_count__lte=(min_tasks_count + 2)),
        is_staff=False,
        is_director=False
    )
    employees_list = []

    for emp in free_employees:
        employees_list.append(emp.full_name)

    result = []

    for task in critical_tasks:
        result.append({"task_title": task.title, "deadline": task.deadline, "employees": employees_list})

    return result
