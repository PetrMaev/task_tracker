from rest_framework import permissions


class IsDirector(permissions.BasePermission):
    """Проверяет, является ли пользователь руководителем."""

    def has_permission(self, request, view):
        if request.user.is_director:
            return True
        return False


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем задачи."""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsExecutor(permissions.BasePermission):
    """Проверяет, является ли пользователь исполнителем задачи."""

    def has_object_permission(self, request, view, obj):
        if obj.executor == request.user:
            return True
        return False


class IsUserOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем своего профиля."""

    def has_object_permission(self, request, view, obj):
        if obj.email == request.user.email:
            return True
        return False
