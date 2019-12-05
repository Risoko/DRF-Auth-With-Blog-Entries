from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission

from .models import DataForAuthenticateUsers

class EmailAuthBackend(ModelBackend):

    def authenticate(self, request, email, password, **kwargs):
        try:
            user = DataForAuthenticateUsers.objects.get(email=email)
        except DataForAuthenticateUsers.DoesNotExist:
            return
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user    