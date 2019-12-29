from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet, ModelViewSet
from rest_framework.authtoken.models import Token

from .serializers import AuthTokenSerializer, RegisterSerializer, ResetPasswordSerializer, CreateProfileUserSerializer, AccountDetailSerializer, AccountChangePassword, AccountChangeEmail
from .models import DataForAuthenticateUsers, PersonalUsersData, User
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
        user = User.objects.get(user_authenticate_date=data_auth_user)
        serializer = self.get_serializer_class()(user.user_personal_data)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth_data = request.user
        user = User.objects.get(user_authenticate_date=auth_data.id)
        user.user_personal_data = serializer.save()
        user.save()
        return Response(
            data=serializer.data, 
            status=status.HTTP_201_CREATED
        )

    @action(methods=['PUT'], detail=False)
    def reset_password(self, request, *args, **kwargs):
        return self.reset_schema(request, *args, **kwargs)

    @action(methods=['PUT'], detail=False)
    def reset_email(self, request, *args, **kwargs):
        return self.reset_schema(request, *args, **kwargs)

    def reset_schema(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def get_serializer_class(self):
        if self.action == "list":
            return  AccountDetailSerializer
        elif self.action == "reset_password":
            return AccountChangePassword
        elif self.action == "reset_email":
            return AccountChangeEmail
        elif self.action == "create":
            return CreateProfileUserSerializer










