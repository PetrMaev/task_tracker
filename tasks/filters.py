from django_filters import BooleanFilter, CharFilter, FilterSet

from tasks.models import Task


class TaskFilter(FilterSet):
    """Фильтрует задачи не взятые в работу, но от которых зависят другие задачи"""

    status = CharFilter(field_name="status", lookup_expr="icontains", label="Статус задачи")
    is_parent = BooleanFilter(field_name="is_parent", label="Признак родительской задачи")

    class Meta:
        model = Task
        fields = []
