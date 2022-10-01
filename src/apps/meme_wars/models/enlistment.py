from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.common.models import BaseModel


class Enlistment(BaseModel):
    class Meta:
        verbose_name = _('Enlistment')
        verbose_name_plural = _('Enlistments')

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_('user'),
        related_name='enlistments',
    )
    war = models.ForeignKey(
        to='meme_wars.War',
        on_delete=models.PROTECT,
        verbose_name=_('war'),
        related_name='enlistments',
    )

    def __str__(self):
        return f'"{self.war.name}" enlistment for "{self.user}"'
