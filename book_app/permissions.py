from rest_framework import permissions
from user_app.models import EntityChoices

class LibrarianPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.entity != EntityChoices.LIBRARIAN : 
            return False
        return super().has_permission(request, view)

class StudentPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.entity != EntityChoices.STUDENT:
            return False
        return super().has_permission(request, view)