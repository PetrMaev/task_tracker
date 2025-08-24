from django.urls import path

from users.apps import UsersConfig
from users.views import CustomUserCreateAPIView, CustomUserListAPIView, CustomUserRetrieveAPIView, \
    CustomUserUpdateAPIView, CustomUserDestroyAPIView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name

urlpatterns = [
    path("users/register/", CustomUserCreateAPIView.as_view(), name="user-register"),
    path("users/", CustomUserListAPIView.as_view(), name="user-list"),
    path("users/<int:pk>/", CustomUserRetrieveAPIView.as_view(), name="user-detail"),
    path("users/<int:pk>/edit/", CustomUserUpdateAPIView.as_view(), name="user-edit"),
    path("users/delete/<int:pk>/", CustomUserDestroyAPIView.as_view(), name="user-delete"),
    path("token/", TokenObtainPairView.as_view(), name="token-obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
