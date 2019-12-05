from string import punctuation

from rest_framework import serializers

from .models import DataForAuthenticateUsers

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        required=True,
        style={
            'input_type': 'password',
            'placeholder': 'Password'
        }
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
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

    def validate_password2(self, password):
        if not self.check_password(password):
            raise serializers.ValidationError(
                detail='Password must have a minimum of 1 upper case letter, 2 digits and 2 special characters.'
            )
        elif len(password) < 8:
            raise serializers.ValidationError(
                detail="This password is too short. It must contain at least 8 characters."
            )
        return password

    def check_password(self, password):
        return all(
            (
                self._checks_password_for_at_least_two_digits(password),
                self._checks_passwords_it_has_at_last_two_special_sign(password),
                self._checks_passwords_it_has_at_least_one_upper_letter(password)
            )
        )

    def validate(self, valide_data):
        password1 = valide_data.get('password1')
        password2 = valide_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError(
                detail="Two password mismatch."
            )
        return valide_data
        
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

    def create(self, validated_data):
        new_data_for_auth = DataForAuthenticateUsers(
            username=validated_data['username'],
            email=validated_data['email']
        )
        new_data_for_auth.set_password(validated_data['password1'])
        new_data_for_auth.save()
        return new_data_for_auth