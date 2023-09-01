from rest_framework import permissions


class IsProfileOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    message = "You can not change this profile"

    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user or 
            request.method in permissions.SAFE_METHODS)