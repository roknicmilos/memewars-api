from django.contrib.postgres.fields import ArrayField

from apps.common.models.singleton_model import SingletonModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserSettings(SingletonModel):
    class Meta:
        verbose_name = _('User Settings')
        verbose_name_plural = _('User Settings')

    allowed_email_domains = ArrayField(
        base_field=models.CharField(
            verbose_name=_('allowed email domains'),
            max_length=500,
        ),
        default=list,
        blank=True,
        help_text=_(
            'Values separated by comma (,). '
            'If left unset, no one will be able to register or login. '
            'If "*" is in the list, everyone will be able to register and login.'
        ),
    )
    allowed_emails = ArrayField(
        base_field=models.CharField(
            verbose_name=_('allowed emails'),
            max_length=500,
        ),
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
