from rest_framework.permissions import BasePermission
import os
import dotenv

dotenv.load_dotenv()


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if os.getenv('DISABLE_AUTH') == 'True':
            return True
        return bool(request.user and request.user.is_authenticated)


class AdminOnly(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_admin


class OnlyAdminCanCreate(BasePermission):
    """
    Only allow POST requests to admin users.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.is_admin
        return True


class OnlyAdminCanUpdate(BasePermission):
    """
    Only allow PUT requests to admin users.
    """

    def has_permission(self, request, view):
        if request.method == 'PUT':
            return request.user and request.user.is_admin
        return True


class OnlyAdminCanDelete(BasePermission):
    """
    Only allow DELETE requests to admin users.
    """

    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user and request.user.is_admin
        return True


class OnlyAdminCanRead(BasePermission):
    """
    Only allow GET requests to admin users.
    """

    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user and request.user.is_admin
        return True
