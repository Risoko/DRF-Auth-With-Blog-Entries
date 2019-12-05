from django.contrib.auth.hashers import check_password

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

    def get_response(self):
        return self.client.post(
            path=reverse(
                viewname='dataforauthenticateusers-list'
            ),
            data=self.data
        )

    def test_with_correct_data(self):
        response = self.get_response()
        self.assertEqual(
            response.data,
            {
                'username': self.data['username'],
                'email': self.data['email']
            }
        )
        self.assertEqual(response.status_code, 201)
        data_for_auth = DataForAuthenticateUsers.objects \
                                                .get(username=self.data['username'])
        self.assertEqual(data_for_auth.username, self.data['username'])
        self.assertEqual(data_for_auth.email, self.data['email'])
        self.assertTrue(check_password(
                password=self.data['password1'],
                encoded=data_for_auth.password
            )
        )
        

