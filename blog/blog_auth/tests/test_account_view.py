from datetime import datetime

from django.contrib.auth.hashers import check_password

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token

from blog_auth.models import DataForAuthenticateUsers, User

class TestAccountView(APITestCase):
    def setUp(self):
        self.create_data = {
            "birth_day": 12,
            "birth_month": 10,
            "birth_year": 1996,
            "first_name": "Przemyslaw",
            "last_name": "Rozycki",
            "nick": "TeKa",
            "country": "PL",
            "sex": "M",
        }
        self.change_password_data = {
            "old_password": "Tester1996.,",
            "new_password1": "NewPassword12.,",
            "new_password2": "NewPassword12.,"
        }
        self.change_email_data = {
            "old_email": "tester@example.com",
            "new_email1": "new_email@example.com",
            "new_email2": "new_email@example.com",
        }
        self.data_for_auth = DataForAuthenticateUsers(
            username="tester1996",
            email="tester@example.com"
        )
        self.data_for_auth.set_password("Tester1996.,")
        self.data_for_auth.save()
        self.user = User(
            user_authenticate_date=self.data_for_auth
        ) 
        self.user.save()
        self.token, _= Token.objects.get_or_create(user=self.data_for_auth)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_account_with_correct_data(self):
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                "first_name": self.create_data['first_name'],
                "last_name": self.create_data['last_name'],
                "nick": self.create_data['nick'],
                "country": self.create_data['country'],
                "sex": self.create_data['sex'],
                "date_birth": '1996-10-12'
            }
        )
        response_items = dict(response.items())
        self.assertEqual(
            response_items['Content-Type'],
            "application/json"
        )
        self.assertEqual(
            response_items['Allow'],
            'GET, POST, HEAD, OPTIONS'
        )

    def test_create_account_when_first_name_is_empty(self):
        del self.create_data['first_name']
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['first_name'][0],
            "This field is required."
        )

    def test_create_account_when_first_name_has_digits(self):
        self.create_data['first_name'] = "BadName123"
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['first_name'][0],
            "First name must contain only letters."
        )

    def test_create_account_when_first_name_has_punctuation_sign(self):
        self.create_data['first_name'] = "BadName.,"
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['first_name'][0],
            "First name must contain only letters."
        )

    def test_create_account_when_first_name_contains_different_letter_sizes(self):
        self.create_data['first_name'] = "TesTerOwski"
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["first_name"],
            self.create_data["first_name"].capitalize()
        )

    def test_create_account_when_first_name_is_too_long(self):
        self.create_data['first_name'] = 100 * "TooLongName"
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['first_name'][0],
            "Ensure this field has no more than 120 characters."
        )

    def test_create_account_when_first_name_is_too_short(self):
        self.create_data['first_name'] = "g"
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['first_name'][0],
            "Ensure this field has at least 3 characters."
        )

    def test_create_account_when_last_name_is_empty(self):
        del self.create_data['last_name']
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['last_name'][0],
            "This field is required."
        )

    def test_create_account_when_last_name_has_digits(self):
        self.create_data['last_name'] = "BadName123"
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['last_name'][0],
            "Last name must contain only letters."
        )

    def test_create_account_when_last_name_has_punctuation_sign(self):
        self.create_data['last_name'] = "BadName.,"
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['last_name'][0],
            "Last name must contain only letters."
        )

    def test_create_account_when_last_name_contains_different_letter_sizes(self):
        self.create_data['last_name'] = "TesTerOwski"
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["last_name"],
            self.create_data["last_name"].capitalize()
        )

    def test_create_account_when_last_name_is_too_long(self):
        self.create_data['last_name'] = 100 * "TooLongName"
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['last_name'][0],
            "Ensure this field has no more than 120 characters."
        )

    def test_create_account_when_last_name_is_too_short(self):
        self.create_data['last_name'] = "g"
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['last_name'][0],
            "Ensure this field has at least 3 characters."
        )

    def test_create_account_when_nick_is_empty(self):
        del self.create_data['nick']
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['nick'][0],
            "This field is required."
        )

    def test_create_account_when_nick_is_digits(self):
        self.create_data['nick'] = "323232123"
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['nick'][0],
            'Nick can not be just a number.'
        )

    def test_create_account_when_nick_is_too_long(self):
        self.create_data['nick'] = 100 * "TooLongNick"
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['nick'][0],
            "Ensure this field has no more than 120 characters."
        )

    def test_create_account_when_nick_is_too_short(self):
        self.create_data['nick'] = "g"
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['nick'][0],
            "Ensure this field has at least 3 characters."
        )

    def test_create_account_when_nick_is_taken_by_another_user(self):
        for _ in range(2):
            response = self.client.post(
                path=reverse("account_user-list"),
                data=self.create_data
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['nick'][0],
            "A user with that nick already exists."
        )

    def test_create_account_when_birth_day_is_too_big(self):
        self.create_data['birth_day'] = 100
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['birth_day'][0],
            "Ensure this value is less than or equal to 31."
        )

    def test_create_account_when_birth_day_is_too_small(self):
        self.create_data['birth_day'] = 0
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['birth_day'][0],
            "Ensure this value is greater than or equal to 1."
        )

    def test_create_account_when_birth_day_is_string(self):
        self.create_data['birth_day'] = "sdss"
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['birth_day'][0],
            "A valid integer is required."
        )

    def test_create_account_when_birth_year_is_too_big(self):
        self.create_data['birth_year'] = 100
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['birth_year'][0],
            f"Ensure this value is greater than or equal to {datetime.now().year - 100}."
        )

    def test_create_account_when_birth_year_is_too_small(self):
        self.create_data['birth_year'] = 2021
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['birth_year'][0],
            f"Ensure this value is less than or equal to {datetime.now().year - 5}."
        )

    def test_create_account_when_birth_year_is_string(self):
        self.create_data['birth_year'] = "sdss"
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['birth_year'][0],
            "A valid integer is required."
        )

    def test_create_profile_when_user_is_not_login(self):
        self.client.credentials()
        response = self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()['detail'],
            'Authentication credentials were not provided.'
        )

    def test_change_password_with_correct_data(self):
        response = self.client.put(
            path=reverse("account_user-change-password"),
            data=self.change_password_data
        )
        self.assertEqual(response.status_code, 200)
        auth_data = DataForAuthenticateUsers.objects.get(username="tester1996")
        self.assertTrue(
            check_password(
                password=self.change_password_data['new_password1'],
                encoded=auth_data.password
            )
        )
        response_items = dict(response.items())
        self.assertEqual(
            response_items['Content-Type'],
            "application/json"
        )
        self.assertEqual(
            response_items['Allow'],
            'PUT, OPTIONS'
        )

    def test_change_password_when_old_password_is_empty(self):
        del self.change_password_data['old_password']
        response = self.client.put(
            path=reverse("account_user-change-password"),
            data=self.change_password_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['old_password'][0],
            "This field is required."
        )

    def test_change_password_when_old_password_is_bad(self):
        self.change_password_data['old_password'] = 'bad_old_password'
        response = self.client.put(
            path=reverse("account_user-change-password"),
            data=self.change_password_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['old_password'][0],
            "Old password mismatch."
        )

    def test_change_password_with_empty_new_password1_field(self):
        del self.change_password_data['new_password1']
        response = self.client.put(
            path=reverse("account_user-change-password"),
            data=self.change_password_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['new_password1'][0], 
            "This field is required."
        )

    def test_change_password_with_empty_password2_field(self):
        del self.change_password_data['new_password2']
        response = self.client.put(
            path=reverse("account_user-change-password"),
            data=self.change_password_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['new_password2'][0], 
            "This field is required."
        )

    def test_change_password_with_bad_format_password(self):
        self.change_password_data["new_password1"] = "bad_password"
        self.change_password_data["new_password2"] = "bad_password"
        response = self.client.put(
            path=reverse("account_user-change-password"),
            data=self.change_password_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['new_password2'][0],
            "Password must have a minimum of 1 upper case letter, 2 digits and 2 special characters."
        )

    def test_change_password_when_two_password_mismatch(self):
        self.change_password_data['new_password2'] = "Password_mismatch12.,"
        response = self.client.put(
            path=reverse("account_user-change-password"),
            data=self.change_password_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['non_field_errors'][0],
            "Two password mismatch."
        )

    def test_change_password_when_is_too_short(self):
        self.change_password_data['new_password1'] = "T12.,"
        response = self.client.put(
            path=reverse("account_user-change-password"),
            data=self.change_password_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['new_password1'][0], 
            "Ensure this value has at least 8 characters."
        )

    def test_change_password_when_user_is_not_login(self):
        self.client.credentials()
        response = self.client.post(
            path=reverse("account_user-change-password"),
            data=self.change_password_data
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()['detail'],
            'Authentication credentials were not provided.'
        )

    def test_change_email_with_correct_data(self):
        response = self.client.put(
            path=reverse("account_user-change-email"),
            data=self.change_email_data
        )
        self.assertEqual(response.status_code, 200)
        auth_data = DataForAuthenticateUsers.objects.get(username="tester1996")
        self.assertEqual(
            self.change_email_data['new_email1'],
            auth_data.email
        )
        response_items = dict(response.items())
        self.assertEqual(
            response_items['Content-Type'],
            "application/json"
        )
        self.assertEqual(
            response_items['Allow'],
            'PUT, OPTIONS'
        )

    def test_change_email_when_old_email_is_empty(self):
        del self.change_email_data["old_email"]
        response = self.client.put(
            path=reverse("account_user-change-email"),
            data=self.change_email_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["old_email"][0],
            'This field is required.'
        )

    def test_change_email_when_old_email_is_bad(self):
        self.change_email_data["old_email"] = "bad_email@example.com"
        response = self.client.put(
            path=reverse("account_user-change-email"),
            data=self.change_email_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["old_email"][0],
            "Old email mismatch."
        )

    def test_change_email_when_new_email1_field_is_empty(self):
        del self.change_email_data["new_email1"]
        response = self.client.put(
            path=reverse("account_user-change-email"),
            data=self.change_email_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["new_email1"][0],
            "This field is required."
        )

    def test_change_email_when_new_email2_field_is_empty(self):
        del self.change_email_data["new_email2"]
        response = self.client.put(
            path=reverse("account_user-change-email"),
            data=self.change_email_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["new_email2"][0],
            "This field is required."
        )

    def test_change_email_when_new_email1_and_new_email2_field_mismatch(self):
        self.change_email_data["new_email2"] = "mismatch_email@example.com"
        response = self.client.put(
            path=reverse("account_user-change-email"),
            data=self.change_email_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["non_field_errors"][0],
            "Two email mismatch."
        )

    def test_change_email_when_another_user_has_the_same_email(self):
        another_user = DataForAuthenticateUsers(
            email="another_user@gmail.com",
            username="tester1"
        )
        another_user.set_password("testerrrere")
        another_user.save()
        self.change_email_data["new_email2"] = another_user.email
        self.change_email_data["new_email1"] = another_user.email
        response = self.client.put(
            path=reverse("account_user-change-email"),
            data=self.change_email_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["non_field_errors"][0],
            "A user with that e-mail already exists."
        )

    def test_change_email_with_the_same_old_email(self):
        self.change_email_data["new_email1"] = self.change_email_data["old_email"]
        self.change_email_data["new_email2"] = self.change_email_data["old_email"]
        response = self.client.put(
            path=reverse("account_user-change-email"),
            data=self.change_email_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["non_field_errors"][0],
            "A user with that e-mail already exists."
        )

    def test_change_email_with_bad_format_email(self):
        self.change_email_data["new_email1"] = "bad_format"
        self.change_email_data["new_email2"] = "bad_format"
        response = self.client.put(
            path=reverse("account_user-change-email"),
            data=self.change_email_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["new_email2"][0],
            "Enter a valid email address."
        )

    def test_change_email_when_user_is_not_login(self):
        self.client.credentials()
        response = self.client.post(
            path=reverse("account_user-change-email"),
            data=self.change_password_data
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()['detail'],
            'Authentication credentials were not provided.'
        )

    def test_detail_profile_with_user_is_login(self):
        self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        response = self.client.get(
            path=reverse("account_user-list")
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'first_name': 'Przemyslaw', 
                'last_name': 'Rozycki', 
                'nick': 'TeKa', 
                'country': 'PL', 
                'sex': 'M', 
                'date_birth': '1996-10-12', 
                'number_article': 0
            }
        )

    def test_detail_profile_with_user_is_not_login(self):
        self.client.post(
            path=reverse("account_user-list"),
            data=self.create_data
        )
        self.client.credentials()
        response = self.client.get(
            path=reverse("account_user-list")
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()['detail'],
            'Authentication credentials were not provided.'
        )
