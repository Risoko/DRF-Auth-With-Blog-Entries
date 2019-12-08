from django.test import TestCase
from django.contrib.auth.hashers import check_password

from blog_auth.authentication import EmailAuthBackend
from blog_auth.models import DataForAuthenticateUsers


class TestEmailAuthBackend(TestCase):
    
    def setUp(self):
        self.password = 'Tester123,.'
        self.data = {
            'username': 'tester',
            'email': 'tester123@gmail.com',
        }
        self.user = DataForAuthenticateUsers(**self.data)
        self.user.set_password(self.password)
        self.user.save()
        self.backend = EmailAuthBackend

    def with_correct_email(self):
        test = self.backend()
        user = test.authenticate(
            request=None, 
            email=self.data['email'],
            password=self.password
        )
        self.assertEqual(user.email, self.data['email'])
        self.assertEqual(user.username, self.data['username'])
        self.assertTrue(
            check_password(
                password=self.password,
                encoded=user.password
            )
        )

    def test_with_bad_email(self):
        test = self.backend()
        user = test.authenticate(
            request=None, 
            email='bad_email',
            password=self.password
        )
        self.assertIsNone(user)

    def test_with_bad_password(self):
        test = self.backend()
        user = test.authenticate(
            request=None, 
            email=self.data['email'],
            password='bad_password'
        )
        self.assertIsNone(user)
