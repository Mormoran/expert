from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    message = 'You must be the owner of this object.'
    safe_method = ['GET', 'PUT']

    def has_permission(self, request, view):
        if request.method in self.safe_method:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in self.permissions.safe_method:
            return True
        return obj.user == request.user