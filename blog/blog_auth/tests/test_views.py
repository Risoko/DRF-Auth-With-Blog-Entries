from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from blog_auth.models import DataForAuthenticateUsers
from blog_auth.views import RegistrationView

class TestRegistrationView(APITestCase):

    def setUp(self):
        self.data = {
            'username': 'test1996',
            'email': 'test@op.pl',
            'password1': 'Dobre123,.,,',
            'password2': 'Dobre123,.,,',
        }

    def test_with_correct_data(self):
        response = self.client.post('/api_auth/registration', self.data, format='json')
        print(response)

