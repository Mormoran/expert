from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    message = 'Permission denied.'
    safe_method = ['GET', 'PUT', 'POST', 'PATCH']

    def has_permission(self, request, view):
        if request.method in self.safe_method:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in self.permissions.safe_method:
            return True
        return obj.owner == request.user

class IsSensor(BasePermission):

    #Allows access only to sensor group members.
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='Sensor'):
            return True
        return False