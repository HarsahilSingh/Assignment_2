from rest_framework import permissions


class IsLecturer(permissions.BasePermission):
    message = 'you are not a lecturer'

    def has_permission(self, request, view):
        user_groups = request.user.groups.value_list('name', flat=True)
        if 'lecturer' in user_groups:
            return True
        return False


class IsStudent(permissions.BasePermission):
    message = 'you are not a student'

    def has_permission(self, request, view):
        user_groups = request.user.groups.value_list('name', flat=True)
        if 'student' in user_groups:
            return True
        return False