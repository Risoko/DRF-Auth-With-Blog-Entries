from django.contrib.auth.hashers import check_password

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from blog_auth.models import User, DataForAuthenticateUsers


class ResetPasswordView(APITestCase):

    def setUp(self):
        self.data = {
            'username': "tester1996",
            'email': "test_django@gmail.com"
        }
        self.data_for_auth = DataForAuthenticateUsers(
            username="tester1996",
            email="test_django@gmail.com"
        )
        self.data_for_auth.set_password("Tester123.,")
        self.data_for_auth.save()
        self.user = User(
            user_authenticate_date=self.data_for_auth
        )
        self.user.save()

    def test_with_correct_data(self):
        response = self.client.post(
            path=reverse("reset_password-list"),
            data=self.data,
            format='json'
        )
        response_items = dict(response.items())
        self.assertEqual(response.status_code, 200)
        self.data_for_auth = DataForAuthenticateUsers.objects.get(username="tester1996")
        self.assertTrue(
            check_password(
                password=response.json()['password'],
                encoded=self.data_for_auth.password
            )
        )
        self.assertEqual(
            response_items['Content-Type'],
            "application/json"
        )
        self.assertEqual(
            response_items['Allow'],
            'POST, OPTIONS'
        )

    def test_with_empty_username_field(self):
        del self.data['username'] 
        response = self.client.post(
            path=reverse("reset_password-list"),
            data=self.data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['username'][0], 
            'This field is required.'
        )

    def test_with_bad_username_field(self):
        self.data["username"] = "BadUsername"
        response = self.client.post(
            path=reverse("reset_password-list"),
            data=self.data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['non_field_errors'][0], 
            "User about this email or username don't exist."
        )

    def test_with_empty_email_field(self):
        del self.data['email'] 
        response = self.client.post(
            path=reverse("reset_password-list"),
            data=self.data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['email'][0], 
            'This field is required.'
        )

    def test_with_bad_email_field(self):
        self.data["email"] = "BadEmail@gmail.com"
        response = self.client.post(
            path=reverse("reset_password-list"),
            data=self.data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['non_field_errors'][0], 
            "User about this email or username don't exist."
        )



        
