from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError

from apps.common.models.singleton_model import SingletonModel
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.validators import UniqueArrayValuesValidator, AsteriskValidator


class UserSettings(SingletonModel):
    class Meta:
        verbose_name = _('User Settings')
        verbose_name_plural = _('User Settings')

    allowed_email_domains = ArrayField(
        verbose_name=_('allowed email domains'),
        base_field=models.CharField(
            max_length=100
        ),
        validators=[
            UniqueArrayValuesValidator(),
            AsteriskValidator()
        ],
        default=list,
        blank=True,
        help_text=_(
            'Values separated by comma (,). '
            'If left unset, no one will be able to register or login. '
            'If "*" is in the list, everyone will be able to register and login.'
        ),
    )
    allowed_emails = ArrayField(
        verbose_name=_('allowed emails'),
        base_field=models.EmailField(),
        validators=[
            UniqueArrayValuesValidator(),
        ],
        default=list,
        blank=True,
        help_text=_(
            'Values separated by comma (,). '
            'Takes priority over "allowed email domain". '
            'In other words, if the email from this list is not in the "allowed email domains", '
            'the user will still be able to register and login.'
        ),
    )

    def __str__(self):
        return str(self.verbose_name)

    @classmethod
    def validate_email(cls, email: str) -> None:
        user_settings = cls.load()
        email_domain = email.split('@')[-1]
        if email not in user_settings.allowed_emails and email_domain not in user_settings.allowed_email_domains:
            raise ValidationError(_('This email is not allowed'), code='forbidden_email')
