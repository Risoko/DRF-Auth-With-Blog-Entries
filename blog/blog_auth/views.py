from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet, ModelViewSet
from rest_framework.authtoken.models import Token

from .serializers import AuthTokenSerializer, RegisterSerializer, ResetPasswordSerializer, CreateProfileUserSerializer
from .models import DataForAuthenticateUsers, PersonalUsersData
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


class CreateProfileUserView(GenericViewSet,
                            CreateModelMixin,
                            ):
    serializer_class = CreateProfileUserSerializer
    permission_classes = [IsAuthenticated]
    queryset = PersonalUsersData.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        user = request.user
        user.user_personal_data = serializer.save()
        user.save()
        return Response(
            data=serializer.data, 
            status=status.HTTP_201_CREATED
        )


