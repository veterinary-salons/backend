from rest_framework import permissions

from authentication.utils import get_recovery_code


class EmailCodeConfirmed(permissions.BasePermission):
    message = "You haven't confirmed the code from your email letter"

    def has_permission(self, request, view):
        email = request.user.email
        code = get_recovery_code(email)
        return code.confirmed