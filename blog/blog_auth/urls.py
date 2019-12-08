from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import RegistrationView, ObtainAuthToken

router = DefaultRouter()
router.register(r'registration', RegistrationView, basename='registration')
router.register(r'login', ObtainAuthToken, basename='login')

urlpatterns = [
    path('', include(router.urls)),
]
