from rest_framework.permissions import IsAuthenticated


class IsNotAuthenticated(IsAuthenticated):

    def has_permission(self, request, view):
        return not super().has_permission(request, view)
    