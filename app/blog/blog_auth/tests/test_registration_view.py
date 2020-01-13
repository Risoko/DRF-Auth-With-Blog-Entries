from django.contrib.auth.hashers import check_password

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from blog_auth.models import DataForAuthenticateUsers


class TestRegistrationView(APITestCase):

    def setUp(self):
        self.data = {
            "username": "tester1996",
            "email": "tester1996@gmail.com",
            "password1": "Tester1996.,",
            "password2": "Tester1996.,",
        }

    def test_with_correct_data(self):
        response = self.client.post(
            path=reverse("registration-list"),
            data=self.data,
            format="json"
        )
        data_for_auth = DataForAuthenticateUsers.objects.get(
            username=self.data['username']
        )
        self.assertEqual(
            self.data['username'],
            data_for_auth.username
        )
        self.assertEqual(
            self.data['email'],
            data_for_auth.email
        )
        self.assertTrue(
            check_password(
                password=self.data['password1'],
                encoded=data_for_auth.password
            )
        )
        response_items = dict(response.items())
        self.assertEqual(response.status_code, 201)
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
            path=reverse("registration-list"),
            data=self.data,
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['username'][0], 
            "This field is required."
        )

    def test_with_username_field_when_is_too_long(self):
        self.data['username'] = 10 * "too_long_username"
        response = self.client.post(
            path=reverse("registration-list"),
            data=self.data,
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['username'][0], 
            "Ensure this field has no more than 150 characters."
        )

    def test_with_username_field_when_is_too_short(self):
        self.data['username'] = "sh"
        response = self.client.post(
            path=reverse("registration-list"),
            data=self.data,
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['username'][0], 
            "Ensure this value has at least 3 characters."
        )

    def test_with_username_field_when_this_username_is_exists(self):
        for _ in range(2):
            response = self.client.post(
                path=reverse("registration-list"),
                data=self.data,
                format="json"
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['username'][0],
            "A user with that username already exists."
        )

    def test_with_empty_email_field(self):
        del self.data['email']
        response = self.client.post(
            path=reverse("registration-list"),
            data=self.data,
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['email'][0], 
            "This field is required."
        )

    def test_with_bad_format_email(self):
        self.data["email"] = "bad_format_email"
        response = self.client.post(
            path=reverse("registration-list"),
            data=self.data,
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['email'][0],
            "Enter a valid email address."
        )

    def test_with_email_field_when_this_email_is_exists(self):
        for _ in range(2):
            response = self.client.post(
                path=reverse("registration-list"),
                data=self.data,
                format="json"
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['email'][0],
            "A user with that e-mail already exists."
        )


    def test_with_empty_password1_field(self):
        del self.data['password1']
        response = self.client.post(
            path=reverse("registration-list"),
            data=self.data,
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['password1'][0], 
            "This field is required."
        )

    def test_with_empty_password2_field(self):
        del self.data['password2']
        response = self.client.post(
            path=reverse("registration-list"),
            data=self.data,
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['password2'][0], 
            "This field is required."
        )

    def test_with_bad_format_password(self):
        self.data["password1"] = "bad_password"
        self.data["password2"] = "bad_password"
        response = self.client.post(
            path=reverse("registration-list"),
            data=self.data,
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['password2'][0],
            "Password must have a minimum of 1 upper case letter, 2 digits and 2 special characters."
        )

    def test_when_two_password_mismatch(self):
        self.data['password2'] = "Password_mismatch12.,"
        response = self.client.post(
            path=reverse("registration-list"),
            data=self.data,
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['non_field_errors'][0],
            "Two password mismatch."
        )

    def test_with_password_field_when_is_too_short(self):
        self.data['password1'] = "T12.,"
        response = self.client.post(
            path=reverse("registration-list"),
            data=self.data,
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['password1'][0], 
            "Ensure this value has at least 8 characters."
        )