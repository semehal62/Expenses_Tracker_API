from rest_framework.permissions import BasePermission

class IsAuthenticatedAndNotBanned(BasePermission):
    message = "User is banned."

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and not getattr(user, "is_banned", False)
