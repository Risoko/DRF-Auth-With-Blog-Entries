from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import RegistrationView

router = DefaultRouter()
router.register(r'registration', RegistrationView)

urlpatterns = [
    path('', include(router.urls))
]
