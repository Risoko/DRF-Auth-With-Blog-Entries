from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrSuperUserOrReadOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.check_the_owner(request.user)