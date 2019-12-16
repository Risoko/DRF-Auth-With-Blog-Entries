from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import RegistrationView, ObtainAuthToken, ResetPasswordView

router = DefaultRouter()
router.register(r'registration', RegistrationView, basename='registration')
router.register(r'login', ObtainAuthToken, basename='login')
router.register(r'reset_password', ResetPasswordView, basename='reset_password')


urlpatterns = [
    path('', include(router.urls)),
]
