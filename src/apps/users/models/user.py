from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
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
    email = models.EmailField(verbose_name=_("email"), db_collation="case_insensitive", unique=True)
    image_url = models.URLField(verbose_name=_("image URL"), null=True, blank=True)
    username = None

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
