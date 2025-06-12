# permissions.py
from rest_framework.permissions import BasePermission

class IsGroupLeader(BasePermission):
    def has_permission(self, request, view):
        group_id = view.kwargs.get('group_id')
        return request.user.is_authenticated and request.user.groups.filter(id=group_id, leader=request.user).exists()
