from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import RegistrationView, LoginView, ResetPasswordView, AccountView

ROUTER = DefaultRouter()
ROUTER.register(r'registration', RegistrationView, basename='registration')
ROUTER.register(r'login', LoginView, basename='login')
ROUTER.register(r'reset_password', ResetPasswordView, basename='reset_password')
ROUTER.register(r'account', AccountView, basename="account_user")

urlpatterns = [
    path('', include(ROUTER.urls)),
]