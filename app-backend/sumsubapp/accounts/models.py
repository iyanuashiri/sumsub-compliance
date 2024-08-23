from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

# from phonenumber_field.modelfields import PhoneNumberField

from .constants import Message
from .fields import LowerCaseEmailField
from .managers import AccountManager


# Create your models here.


class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=200)
    last_name = models.CharField(_('last name'), max_length=200)
    # phone_number = PhoneNumberField(unique=True, region='NG')
    email = LowerCaseEmailField(
        _('email'),
        unique=True,
        error_messages={
            'unique': Message.NON_UNIQUE_EMAIL.value
        }
    )
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date updated'), auto_now=True)
    is_active = models.BooleanField(
        _('active status'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into the admin site.'),
    )
    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.fullname

    def clean(self):
        super().clean()

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'
