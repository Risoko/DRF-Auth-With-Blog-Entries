from django.test import TestCase
from django.contrib.auth.hashers import check_password

from rest_framework.exceptions import ErrorDetail

from blog_auth.serializers import RegisterSerializer
from blog_auth.models import DataForAuthenticateUsers

class TestRegisterSerializer(TestCase):

    def setUp(self):
        self.serializer = RegisterSerializer
        self.data = {
            'username': 'tester',
            'email': 'tester123@gmail.com',
            'password1': 'DobreHaslo12.,',
            'password2': 'DobreHaslo12.,'
        }
        return self.data

    def get_serializer(self):
        return self.serializer(data=self.data)

    def test_with_correct_data(self):
        serializer = self.get_serializer()
        serializer.is_valid()
        self.assertTrue(serializer.is_valid())
        serializer.save()
        new_user = DataForAuthenticateUsers.objects.get(
            username=self.data['username']
        )
        self.assertEqual(new_user.email, self.data['email'])
        self.assertEqual(new_user.username, self.data['username'])
        self.assertTrue(check_password(
                password=self.data['password1'],
                encoded=new_user.password
            )
        )

    def test_with_empty_username_field(self):
        del self.data["username"]
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['username'][0], 
            'This field is required.'
        )

    def test_with_too_short_username(self):
        self.data['username'] = 'id'
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['username'][0],
            "Ensure this value has at least 3 characters."
        )

    def test_with_too_long_username(self):
        self.data['username'] = 100 * 'aaaa'
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['username'][0]),
            'Ensure this field has no more than 150 characters.'
        )

    def test_with_exist_username(self):
        serializer = self.get_serializer()
        self.assertTrue(serializer.is_valid())
        self.data['email'] = 'correct_email@gmail.com'
        serializer.save()
        serializer2 = self.get_serializer()
        self.assertFalse(serializer2.is_valid())
        self.assertEqual(
            serializer2.errors['username'][0],
            "A user with that username already exists."
        )

    def test_with_empty_email_field(self):
        del self.data["email"]
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['email'][0], 
            'This field is required.'
        )

    def test_with_exist_email(self):
        serializer = self.get_serializer()
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.data['username'] = 'another_username'
        serializer2 = self.get_serializer()
        self.assertFalse(serializer2.is_valid())
        self.assertEqual(
            str(serializer2.errors['email'][0]),
            "A user with that e-mail already exists."
        )

    def test_with_bad_format_email(self):
        serializer = self.get_serializer()
        self.data['email'] = 'bad_format_email'
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['email'][0],
            "Enter a valid email address."
        )

    def test_with_empty_password1_field(self):
        del self.data["password1"]
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['password1'][0], 
            'This field is required.'
        )

    def test_with_empty_password2_field(self):
        del self.data["password2"]
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['password2'][0], 
            'This field is required.'
        )

    def test_with_bad_password_field(self):
        self.data["password2"] = 'bad_password'
        self.data["password2"] = 'bad_password'
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['password2'][0]), 
            'Password must have a minimum of 1 upper case letter, 2 digits and 2 special characters.'
        )

    def test_with_password_too_short(self):
        self.data['password1'] = 'aS12,.'
        self.data['password2'] = 'aS12,.'
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['password2'][0]),
            "This password is too short. It must contain at least 8 characters."
        )

    def test_password_with_only_digit(self):
        self.data['password1'] = '123456789'
        self.data['password2'] = '123456789'
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['password2'][0]),
            'Password must have a minimum of 1 upper case letter, 2 digits and 2 special characters.'
        )

    def test_with_two_different_password(self):
        self.data['password1'] = 'AsfrWE12.,'
        self.data['password2'] = 'AsfrWE12.,,,1'
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['non_field_errors'][0],
            "Two password mismatch."
        )