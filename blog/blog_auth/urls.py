from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import RegistrationView, ObtainAuthToken, ResetPasswordView, CreateProfileUserView

router = DefaultRouter()
router.register(r'registration', RegistrationView, basename='registration')
router.register(r'login', ObtainAuthToken, basename='login')
router.register(r'reset_password', ResetPasswordView, basename='reset_password')
router.register(r'account/create_profile', CreateProfileUserView, basename='create_profile')


urlpatterns = [
    path('', include(router.urls)),
]
