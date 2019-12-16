from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.authtoken.models import Token

from .serializers import AuthTokenSerializer, RegisterSerializer, ResetPasswordSerializer
from .models import DataForAuthenticateUsers
from .permisions import IsNotAuthenticated


class ObtainAuthToken(ViewSet):
    serializer_class = AuthTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class RegistrationView(CreateModelMixin,
                       GenericViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [IsNotAuthenticated, ]


class ResetPasswordView(CreateModelMixin,
                    GenericViewSet):
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsNotAuthenticated]


