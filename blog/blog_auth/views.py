from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializers import RegisterSerializer
from .models import DataForAuthenticateUsers
from .permisions import IsNotAuthenticated

class RegistrationView(CreateModelMixin,
                       GenericViewSet):
    serializer_class = RegisterSerializer
    queryset = DataForAuthenticateUsers.objects.all()
    permissions = [IsNotAuthenticated]