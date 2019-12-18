from datetime import date

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

from pycountry import countries

from .managers import CreateUserProfilManager


class DataForAuthenticateUsers(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(
        verbose_name=_('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that e-mail already exists."),
        }
    )

    class Meta:
        verbose_name = _('Data for authenticate user') 
        verbose_name_plural = _('Data for authenticate users')
        ordering = ['date_joined']


class PersonalUsersData(models.Model):
    MALE_SEX = 'M'
    FEMALE_SEX = 'F'
    SEX_CHOICES = [
        (MALE_SEX, 'Male'),
        (FEMALE_SEX, 'Female')
    ]
    COUNTRY_CHOICES = [(country.alpha_2, country.name) for country in countries]
    first_name = models.CharField(
        max_length=120,
        verbose_name=_('first name'),
        validators=[MinLengthValidator(3)]
    )
    last_name = models.CharField(
        max_length=120,
        verbose_name=_('last name'),
        validators=[MinLengthValidator(3)]
    )
    nick = models.CharField(
        max_length=120,
        verbose_name=_('nick'),
        unique=True,
        validators=[MinLengthValidator(3)],
        error_messages={
            'unique': _("A user with that nick already exists."),
        }
    )
    country = models.CharField(
        max_length=200,
        choices=COUNTRY_CHOICES,
        verbose_name=_('country'),
        default=COUNTRY_CHOICES[79]
    )
    sex = models.CharField(
        max_length=20,
        choices=SEX_CHOICES,
        default=MALE_SEX
    )
    date_birth = models.DateField(
        verbose_name=_('date of birth')
    )
    number_article = models.PositiveSmallIntegerField(
        verbose_name=_('number article'),
        default=0
    )
    objects = CreateUserProfilManager()

    class Meta:
        verbose_name = _('Personal user data')
        verbose_name_plural = _('Personal users data')
        ordering = ['date_birth']


class User(models.Model):
    user_authenticate_date = models.ForeignKey(
        to=DataForAuthenticateUsers,
        on_delete=models.CASCADE,
        related_name='user_fk_auth_data'
    )
    user_personal_data = models.ForeignKey(
        to=PersonalUsersData,
        on_delete=models.SET_NULL,
        related_name='user_fk_personal_data',
        blank=True,
        null=True
    )

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.user_personal_data.first_name,
                               self.user_personal_data.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.user_personal_data.first_name

    def get_nick(self):
        """Return user nick."""
        return self.user_personal_data.nick

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(
            subject=subject,
            message=message, 
            from_email=from_email, 
            recipient_list=[self.user_authenticate_date.email,],
            **kwargs
        )

    def check_is_adult(self):
        """Method check user is adult."""
        date_birth = self.user_personal_data.date_birth
        adult_age = date(
            year=date_birth.year + 18,
            month=date_birth.month,
            day=date_birth.day
        )
        date_now = date(
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        return adult_age <= date_now

    def __str__(self):
        return self.user_authenticate_date.email #f'User(Nick={self.get_nick()}, Fullname={self.get_full_name()})'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users') 
