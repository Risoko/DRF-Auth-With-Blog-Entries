from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.authtoken.models import Token

from .serializers import (
    AuthTokenSerializer, RegisterSerializer, ResetPasswordSerializer,
    AccountDetailSerializer, AccountChangePassword, AccountChangeEmail,
    CreateProfileUserSerializer
)
from .models import User
from .permisions import IsNotAuthenticated


class LoginView(ViewSet):
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
    permission_classes = [IsNotAuthenticated]


class ResetPasswordView(CreateModelMixin,
                        GenericViewSet):
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsNotAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.save()
        return Response(
            data=dict(password=new_password),
            status=status.HTTP_200_OK
        )


class AccountView(GenericViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        data_auth_user = request.user
        user = User.objects.get(user_authenticate_data=data_auth_user)
        serializer = self.get_serializer_class()(user.user_personal_data)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth_data = request.user
        user = User.objects.get(user_authenticate_data=auth_data.id)
        user.user_personal_data = serializer.save()
        user.save()
        data = dict(serializer.data)
        data["date_birth"] = user.user_personal_data.date_birth
        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )

    @action(methods=['PUT'], detail=False)
    def change_password(self, request, *args, **kwargs):
        return self.change_schema(request, *args, **kwargs)

    @action(methods=['PUT'], detail=False)
    def change_email(self, request, *args, **kwargs):
        return self.change_schema(request, *args, **kwargs)

    def change_schema(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def get_serializer_class(self):
        if self.action == "list":
            return  AccountDetailSerializer
        elif self.action == "change_password":
            return AccountChangePassword
        elif self.action == "change_email":
            return AccountChangeEmail
        elif self.action == "create":
            return CreateProfileUserSerializer










