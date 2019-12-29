from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import RegistrationView, LoginView, ResetPasswordView, AccountView

router = DefaultRouter()
router.register(r'registration', RegistrationView, basename='registration')
router.register(r'login', LoginView, basename='login')
router.register(r'reset_password', ResetPasswordView, basename='reset_password')
router.register(r'account', AccountView, basename="account_user")


urlpatterns = [
    path('', include(router.urls)),
]
