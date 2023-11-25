from rest_framework import permissions


class IsEmailConfirmed(permissions.BasePermission):
    message = "Вы не подтвердили код из письма по электронной почте."

    def has_permission(self, request, view):
        return request.user.email_confirmed
