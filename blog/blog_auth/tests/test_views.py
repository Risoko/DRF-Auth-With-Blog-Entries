from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.hashers import check_password

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token

from blog_auth.models import DataForAuthenticateUsers
from blog_auth.views import RegistrationView


class ResponseMixIn:

    def get_response(self, viewname):
        return self.client.post(
            path=reverse(
                viewname=viewname
            ),
            data=self.data
        )



class TestRegistrationView(APITestCase,
                           ResponseMixIn):

    def setUp(self):
        self.data = {
            'username': 'test1996',
            'email': 'test@op.pl',
            'password1': 'Dobre123,.,,',
            'password2': 'Dobre123,.,,',
        }
        self.factory = APIRequestFactory()

    def test_with_correct_data(self):
        response = self.get_response(viewname='registration-list')
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
        self.assertNotIsInstance(data_for_auth, AnonymousUser)
        self.assertEqual(data_for_auth.username, self.data['username'])
        self.assertEqual(data_for_auth.email, self.data['email'])
        self.assertTrue(
            check_password(
                password=self.data['password1'],
                encoded=data_for_auth.password
            )
        )


class TestLoginView(APITestCase,
                    ResponseMixIn):

    def setUp(self):
        self.registr_data = {
            'username': 'tester',
            'email': 'tester123@gmail.com',
        }
        self.data = {
            'username_or_email': self.registr_data['username'],
            'password': 'Tester123,,.'
        }
        self.user = DataForAuthenticateUsers(**self.registr_data)
        self.user.set_password(self.data['password'])
        self.user.save()

    def test_login_with_correct_username(self):
        self.get_response('login-list')
        token = Token.objects.get(user__username=self.data['username_or_email'])
        self.assertEqual(token.user.username, self.data['username_or_email'])
        self.assertEqual(token.user.email, self.registr_data['email'])

    def test_login_with_correct_email(self):
        self.data['username_or_email'] = self.registr_data['email']
        self.get_response('login-list')
        token = Token.objects.get(user__email=self.data['username_or_email'])
        self.assertEqual(token.user.email, self.data['username_or_email'])
        self.assertEqual(token.user.username, self.registr_data['username'])


