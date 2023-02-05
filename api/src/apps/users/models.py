from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.contrib.postgres.fields import CIEmailField
from django.utils.translation import gettext_lazy as _
from apps.common.models import BaseModel


class UserManager(BaseUserManager):

    def create_superuser(self, email: str = None, **kwargs):
        return self._create_user(email=email, is_staff=True, is_superuser=True, **kwargs)

    def create_user(self, email: str = None, **kwargs):
        return self._create_user(email=email, is_staff=False, is_superuser=False, **kwargs)

    def _create_user(self, email: str = None, password: str = None, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.update(password=make_password(password))
        return user


class User(BaseModel, AbstractUser):
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    objects = UserManager()

    email = CIEmailField(
        verbose_name=_('email'),
        db_index=True,
        unique=True
    )
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
