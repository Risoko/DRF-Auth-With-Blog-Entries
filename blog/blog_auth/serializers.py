from datetime import datetime
from random import sample
from string import ascii_uppercase, digits, punctuation

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import DataForAuthenticateUsers, User, PersonalUsersData

class PasswordValidator:

    def __init__(self, min_size):
        self.min_size = min_size

    def __call__(self, password):
        if not self.check_password(password):
            raise serializers.ValidationError(
                detail='Password must have a minimum of 1 upper case letter, 2 digits and 2 special characters.'
            )
        if len(password) < self.min_size:
            msg = f"Ensure this value has at least {self.min_size} characters."
            raise serializers.ValidationError(
                detail=msg
            )

    def check_password(self, password):
        return all(
            (
                self._checks_password_for_at_least_two_digits(password),
                self._checks_passwords_it_has_at_last_two_special_sign(password),
                self._checks_passwords_it_has_at_least_one_upper_letter(password),
            )
        )

    def _checks_password_for_at_least_two_digits(self, password):
        """
        Method return true if the password contains at least two digits.
        """
        return len(list(sign for sign in password if sign.isdigit())) >= 2

    def _checks_passwords_it_has_at_least_one_upper_letter(self, password):
        """
        Method return true if the password contains at least one upper letter.
        """
        return any(sign.isupper() for sign in password)

    def _checks_passwords_it_has_at_last_two_special_sign(self, password):
        """
        Method return true if the password contains at least two special sign.
        """
        return len(list(sign for sign in password if sign in punctuation)) >= 2


class AuthTokenSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(label=_("Username or email"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        password = attrs.get('password')
        username_or_email = attrs.get('username_or_email')
        if username_or_email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username_or_email,
                email=username_or_email,
                password=password
            )
        else:
            msg = _('Must include "username" or "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        required=True,
        trim_whitespace=False,
        validators=[PasswordValidator(8)],
        style={
            'input_type': 'password',
            'placeholder': 'Password'
        }
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[PasswordValidator(8)],
        trim_whitespace=False,
        style={
            'input_type': 'password',
            'placeholder': 'Repeat password'
        }
    )

    class Meta:
        model = DataForAuthenticateUsers
        fields = ['username', 'email', 'password1', 'password2']

    def validate_username(self, username):
        if len(username) < 3:
            raise serializers.ValidationError(
                detail=f"Ensure this value has at least 3 characters."
            )
        return username

    def validate(self, validated_data):
        password1 = validated_data.get('password1')
        password2 = validated_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError(
                detail="Two password mismatch."
            )
        return validated_data
        
    def create(self, validated_data):
        new_data_for_auth = DataForAuthenticateUsers(
            username=validated_data['username'],
            email=validated_data['email']
        )
        new_data_for_auth.set_password(validated_data['password1'])
        new_data_for_auth.save()
        user = User(user_authenticate_date=new_data_for_auth)
        user.save()
        return new_data_for_auth


class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True
    )
    email = serializers.CharField(
        required=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        try:
            user_auth_data = DataForAuthenticateUsers.objects.get(
                username=username,
                email=email
            )
        except DataForAuthenticateUsers.DoesNotExist:
            raise serializers.ValidationError(
                detail="User about this email or username don't exist."
            )
        attrs['user_auth_data'] = user_auth_data
        return attrs

    def get_new_password(self, password_lenght=10):
        """
        The method returns a new random user password.
        """
        numbers = ''.join(sample(digits, 2))
        special_sign = ''.join(sample(punctuation, 2))
        rest_password = ''.join(sample(ascii_uppercase, password_lenght - 4))
        return rest_password + numbers + special_sign

    def save(self):
        user_auth_data = self.validated_data['user_auth_data']
        user = User.objects.get(user_authenticate_date=user_auth_data.id)
        new_password = self.get_new_password()
        user_auth_data.set_password(new_password)
        user_auth_data.save()
        message = f"""
        Hi {user_auth_data.username}.
        You reset your password.
        Your new password: {new_password}
        To change the password, enter in the user profile.
        Regards, blog administration.
        """
        user.email_user(
            subject='Password Reset',
            message=message,
            from_email="Administration blog."
        )
        return new_password


class CreateProfileUserSerializer(serializers.ModelSerializer):
    birth_day = serializers.IntegerField(
        min_value=1,
        max_value=31,
        write_only=True  
    )
    birth_month = serializers.ChoiceField(
        choices=[(number, number) for number in range(1, 13)],
        write_only=True
    )
    birth_year = serializers.IntegerField(
        min_value=datetime.now().year - 100,
        max_value=datetime.now().year - 5,
        write_only=True
    )
    class Meta:
        model = PersonalUsersData
        fields = [
            'first_name', 'last_name',
            'nick', 'country', 'sex',
            'birth_day', 'birth_month',
            'birth_year'
        ]

    def validate_nick(self, data):
        if data.isdigit():
            raise serializers.ValidationError(
                detail='Nick can not be just a number.'
            )
        return data

    def validate_first_name(self, data):
        if not data.isalpha():
            raise serializers.ValidationError(
                detail="First name must contain only letters."
            )

        return data.capitalize()

    def validate_last_name(self, data):
        if not data.isalpha():
            raise serializers.ValidationError(
                detail="Last name must contain only letters."
            )
        return data.capitalize()

    def create(self, validated_data):
        return PersonalUsersData.objects.create_profile(**validated_data)


class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalUsersData
        exclude = ['id']

class AccountChangePassword(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        trim_whitespace=False,
        style={
            'input_type': 'password',
            'placeholder': 'Password'
        }
    )
    new_password1 = serializers.CharField(
        write_only=True,
        required=True,
        trim_whitespace=False,
        style={
            'input_type': 'password',
            'placeholder': 'Password'
        }
    )
    new_password2 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[PasswordValidator(8)],
        style={
            'input_type': 'password',
            'placeholder': 'Repeat password'
        }
    )

    def validate(self, validated_data):
        password1 = validated_data.get('password1')
        password2 = validated_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError(
                detail="Two password mismatch."
            )
        return validated_data

    def validate_old_password(self, data):
        user_auth_data = self.context.get('request').user
        if not check_password(password=data, encoded=user_auth_data.password):
            raise serializers.ValidationError(
                detail="Old password mismatch."
            )
        return user_auth_data

    def save(self):
        user_auth_data = self.validated_data['old_password']
        user_auth_data.set_password(self.validated_data['new_password2'])
        user_auth_data.save()
        user = User.objects.get(user_authenticate_date=user_auth_data.id)
        user.email_user(
            subject="Change Password.",
            message="You have changed password if you do not urgently reset the password",
            from_email="Blog administration."
        )


class AccountChangeEmail(serializers.Serializer):
    old_email = serializers.EmailField()
    new_email = serializers.EmailField()

    def validate_old_email(self, data):
        user_auth_data = self.context.get('request').user
        if user_auth_data.email != data:
            raise serializers.ValidationError(
                detail="Old email mismatch."
            )

    def save(self):
        user_auth_data = self.validated_data['old_email']
        user_auth_data.email = self.validated_data['new_mail']
        user_auth_data.save()
        user = User.objects.get(user_authenticate_date=user_auth_data.id)
        user.email_user(
            subject="Change Email.",
            message="You have changed email if you do not urgently write to support.",
            from_email="Blog administration."
        )





        
    