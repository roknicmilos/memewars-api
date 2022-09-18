from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.common.models import BaseModel
from apps.meme_wars.models import War


class Vote(BaseModel):
    class Meta:
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='votes',
    )
    meme = models.ForeignKey(
        to='meme_wars.Meme',
        on_delete=models.CASCADE,
        verbose_name=_('meme'),
        related_name='votes',
    )
    score = models.ForeignKey(
        to='meme_wars.VotingScore',
        on_delete=models.CASCADE,
        verbose_name=_('score'),
        related_name='votes',
        null=True,
        blank=True,
    )
    submission_count = models.IntegerField(
        verbose_name=_('total submissions'),
        default=1,
    )

    def __str__(self):
        return str(_(f'Vote {self.pk}'))

    def clean(self):
        if self.meme.enlistment.war.has_ended:
            raise ValidationError({'meme': _('You can\'t vote for a meme from a war that has ended')})

    @property
    def score_order(self) -> int | None:
        return self.score.order if self.score else None

    @property
    def war(self) -> War:
        return self.meme.war
