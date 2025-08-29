from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tasks.paginators import CustomPagination
from users.models import CustomUser
from users.permissions import IsUserOwner
from users.serializers import FreeUserSerializer, UserCreateSerializer, UserSerializer
from users.services import get_free_employees


class CustomUserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class CustomUserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]


class CustomUserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["full_name", "email"]
    ordering_fields = ["id", "email", "full_name", "post"]

    def get(self, request, *args, **kwargs):
        allowed_ordering = ["id", "email", "full_name", "tasks", "tasks_count", "-tasks_count", "tasks_active_count",
                            "-tasks_active_count"]

        users = CustomUser.objects.annotate(
            tasks_count=Count("tasks"), tasks_active_count=Count("tasks", filter=Q(tasks__status="work"))
        )
        users_sort = users.filter(is_staff=False)

        ordering = request.query_params.get("ordering")
        if ordering not in allowed_ordering:
            ordering = "id"  # Значение по умолчанию

        sort_users = users_sort.order_by(ordering)

        serializer = UserSerializer(sort_users, many=True)
        return Response(serializer.data)


class FreeEmployeesListAPIView(generics.ListAPIView):
    serializer_class = FreeUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        result = get_free_employees()
        serializer = FreeUserSerializer(result, many=True)
        return Response(serializer.data)


class CustomUserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsUserOwner]


class CustomUserDestroyAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsUserOwner]
