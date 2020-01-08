from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token

from blog_auth.models import DataForAuthenticateUsers, User


class TestLoginView(APITestCase):
    def setUp(self):
        self.data = {
            "username_or_email": "tester1996",
            "password": "Tester123.,"
        }
        data_for_auth = DataForAuthenticateUsers(
            username="tester1996",
            email="test_django@gmail.com"
        )
        data_for_auth.set_password("Tester123.,")
        data_for_auth.save()
        self.user = User(
            user_authenticate_data=data_for_auth
        ) 
        self.user.save()
        self.token, _= Token.objects.get_or_create(user=data_for_auth)

    def test_with_correct_username_and_password(self):
        response = self.client.post(
            path=reverse("login-list"),
            data=self.data,
            format="json"
        )
        response_items = dict(response.items())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['token'], self.token.key)
        self.assertEqual(
            response_items['Content-Type'],
            "application/json"
        )
        self.assertEqual(
            response_items['Allow'],
            'POST, OPTIONS'
        )

    def test_with_correct_email_and_password(self):
        self.data["username_or_email"] = "test_django@gmail.com"
        response = self.client.post(
            path=reverse("login-list"),
            data=self.data,
            format="json"
        )
        response_items = dict(response.items())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['token'], self.token.key)
        self.assertEqual(
            response_items['Content-Type'],
            "application/json"
        )
        self.assertEqual(
            response_items['Allow'],
            'POST, OPTIONS'
        )
        
    def test_with_bad_username(self):
        self.data['username_or_email'] = 'bad_username'
        response = self.client.post(
            path=reverse("login-list"),
            data=self.data,
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['non_field_errors'][0], 
            'Unable to log in with provided credentials.'
        )

    def test_with_bad_email(self):
        self.data['username_or_email'] = 'bad_email@gmail.com'
        response = self.client.post(
            path=reverse("login-list"),
            data=self.data,
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['non_field_errors'][0], 
            'Unable to log in with provided credentials.'
        )

    def test_with_bad_password(self):
        self.data['password'] = 'bad_password'
        response = self.client.post(
            path=reverse("login-list"),
            data=self.data,
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['non_field_errors'][0], 
            'Unable to log in with provided credentials.'
        )

    def test_with_empty_username_or_email_field(self):
        del self.data['username_or_email']
        response = self.client.post(
            path=reverse("login-list"),
            data=self.data,
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['username_or_email'][0], 
            'This field is required.'
        )

    def test_with_empty_password_field(self):
        del self.data['password']
        response = self.client.post(
            path=reverse("login-list"),
            data=self.data,
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['password'][0], 
            'This field is required.'
        )
