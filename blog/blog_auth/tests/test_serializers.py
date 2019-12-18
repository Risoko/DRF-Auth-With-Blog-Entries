from datetime import datetime

from django.test import TestCase
from django.contrib.auth.hashers import check_password

from blog_auth.serializers import (
AuthTokenSerializer, RegisterSerializer, ResetPasswordSerializer, CreateProfileUserSerializer
)
from blog_auth.models import DataForAuthenticateUsers, User, PersonalUsersData


class SerializerMixIn:

    def get_serializer(self):
        return self.serializer(data=self.data)


class TestRegisterSerializer(TestCase, 
                             SerializerMixIn):

    def setUp(self):
        self.serializer = RegisterSerializer
        self.data = {
            'username': 'tester',
            'email': 'tester123@gmail.com',
            'password1': 'DobreHaslo12.,',
            'password2': 'DobreHaslo12.,'
        }
        return self.data

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
        self.assertTrue(
            check_password(
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


class TestAuthTokenSerializer(TestCase,
                              SerializerMixIn):
    
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
        self.serializer = AuthTokenSerializer

    def test_login_with_correct_username_and_password(self):
        serializer = self.get_serializer()
        self.assertTrue(serializer.is_valid())
        user = serializer.validated_data['user']
        self.assertEqual(user.username, self.registr_data['username'])
        self.assertEqual(user.email, self.registr_data['email'])
        self.assertTrue(check_password(
            password=self.data['password'],
            encoded=user.password
        ))

    def test_login_with_correct_email_and_password(self):
        self.data['username_or_email'] = self.registr_data['email']
        serializer = self.get_serializer()
        self.assertTrue(serializer.is_valid())
        user = serializer.validated_data['user']
        self.assertEqual(user.username, self.registr_data['username'])
        self.assertEqual(user.email, self.registr_data['email'])
        self.assertTrue(
            check_password(
                password=self.data['password'],
                encoded=user.password
            )
        )

    def test_with_bad_login_or_email(self):
        self.data['username_or_email'] = "bad_login_or_email"
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["non_field_errors"][0]), 
            'Unable to log in with provided credentials.'
        )

    def test_with_bad_password(self):
        self.data['password'] = "bad_password"
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["non_field_errors"][0]), 
            'Unable to log in with provided credentials.'
        )

    def test_with_empty_username_or_email_field(self):
        del self.data['username_or_email']
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["username_or_email"][0]), 
            'This field is required.'
        )

    def test_with_empty_password_field(self):
        del self.data['password']
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["password"][0]), 
            'This field is required.'
        )


class TestResetPasswordSerializer(TestCase,
                                  SerializerMixIn):

    def setUp(self):
        self.data = {
            'username': 'Tester',
            'email': 'maria.pazdziora1998@gmail.com'
        }
        self.serializer = ResetPasswordSerializer
        self.user_auth = DataForAuthenticateUsers(**self.data)
        self.user_auth.set_password("Testter123.,")
        self.user_auth.save()
        self.user = User(user_authenticate_date=self.user_auth)
        self.user.save()

    def test_with_correct_data(self):
        serializer = self.get_serializer()
        self.assertTrue(serializer.is_valid())
        new_password = serializer.save()
        user_auth = DataForAuthenticateUsers.objects.get(username=self.data['username'])
        self.assertTrue(
            check_password(
                password=new_password,
                encoded=user_auth.password
            )
        )

    def test_with_bad_username(self):
        self.data['username'] = 'bad_username'
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["non_field_errors"][0]), 
            "User about this email or username don't exist."
        )

    def test_with_bad_email(self):
        self.data['email'] = 'bad_email'
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["non_field_errors"][0]), 
            "User about this email or username don't exist."
        )

    def test_with_empty_email_field(self):
        del self.data['email']
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["email"][0]), 
            "This field is required."
        )

    def test_with_empty_username_field(self):
        del self.data['username']
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["username"][0]), 
            "This field is required."
        )


class TestCreateUserProfileSerialiser(TestCase,
                                      SerializerMixIn):
    
    def setUp(self):
        self.data = {
            "first_name": 'Przemyslaw',
            "last_name": "Rozycki",
            "nick": "Tester",
            "country": "Pl",
            "sex": "M",
            "birth_day": "12",
            "birth_month": "March",
            "birth_year": "1996"
        }
        self.serializer = CreateProfileUserSerializer

    def test_with_correct_data(self):
        serializer = self.get_serializer()
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(
            serializer.validated_data,
            self.data
        )

    def test_with_empty_first_name(self):
        del self.data["first_name"]
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["first_name"][0]), 
            "This field is required."
        )

    def test_with_first_name_when_letters_are_not_the_same(self):
        self.data["first_name"] = "PrzEmYslaw"
        serializer = self.get_serializer()
        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            self.data['first_name'].capitalize(),
            serializer.validated_data['first_name']
        )

    def test_with_first_name_too_short(self):
        self.data["first_name"] = 'It'
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['first_name'][0]),
            "Ensure this value has at least 3 characters."
        )

    def test_with_first_name_too_long(self):
        self.data["first_name"] = 'It' * 100
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['first_name'][0]),
            'Ensure this field has no more than 150 characters.'
        )

    def test_when_first_name_has_digits(self):
        self.data["first_name"] = "Przemyslaw123"
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["first_name"][0]),
            "First name must contain only letters."
        )
    
    def test_when_first_name_has_special_sign(self):
        self.data["first_name"] = "Przemys_law"
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["first_name"][0]),
            "First name must contain only letters."
        )
    def test_with_empty_last_name(self):
        del self.data["last_name"]
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["last_name"][0]), 
            "This field is required."
        )

    def test_with_last_name_when_letters_are_not_the_same(self):
        self.data["last_name"] = "RoZycki"
        serializer = self.get_serializer()
        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            self.data['last_name'].capitalize(),
            serializer.validated_data['last_name']
        )

    def test_with_last_name_too_short(self):
        self.data["last_name"] = 'It'
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['last_name'][0]),
            "Ensure this value has at least 3 characters."
        )

    def test_with_last_name_too_long(self):
        self.data["last_name"] = 'It' * 100
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['last_name'][0]),
            'Ensure this field has no more than 150 characters.'
        )

    def test_when_last_name_has_digits(self):
        self.data["last_name"] = "Rozycki123"
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["last_name"][0]),
            "Last name must contain only letters."
        )
    
    def test_when_last_name_has_special_sign(self):
        self.data["last_name"] = "Rozyc_ki"
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["last_name"][0]),
            "Last name must contain only letters."
        )

    def test_with_nick_too_short(self):
        self.data["nick"] = 'It'
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['nick'][0]),
            "Ensure this value has at least 3 characters."
        )

    def test_with_nick_too_long(self):
        self.data["nick"] = 'It' * 100
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['nick'][0]),
            'Ensure this field has no more than 150 characters.'
        )

    def test_nick_when_is_digit(self):
        self.data["nick"] = "123456"
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['nick'][0]),
            'Nick can not be just a number.'
        )

    def test_with_exist_nick(self):
        serializer = self.get_serializer()
        self.assertTrue(serializer.is_valid())
        serializer.save()
        serializer2 = self.get_serializer()
        self.assertFalse(serializer2.is_valid())
        self.assertEqual(
            serializer2.errors['nick'][0],
            "A user with that nick already exists."
        )

    def test_when_birth_day_is_letter(self):
        self.data["birth_day"] = "as"
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['birth_day'][0]),
            "This field must contain only digit."
        )

    def test_when_birth_day_is_too_big(self):
        self.data["birth_day"] = "32"
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['birth_day'][0]),
            "A month has a maximum of 31 days."
        )

    def test_when_birth_day_is_too_small(self):
        self.data["birth_day"] = "0"
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['birth_day'][0]),
            "A month has a minimum of 1 day."
        )

    def test_when_birth_year_is_letter(self):
        self.data["birth_year"] = "as"
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['birth_year'][0]),
            "This field must contain only digit."
        )

    def test_when_birth_year_is_too_big(self):
        self.data["birth_year"] = str(datetime.now().year)
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['birth_year'][0]),
            "You couldn't have been born this year (is too big)."
        )

    def test_when_birth_year_is_too_small(self):
        self.data["birth_year"] = str(datetime.now().year - 110)
        serializer = self.get_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['birth_year'][0]),
            "You couldn't have been born this year (is too small)."
        )





    
        
        

