from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.models import BaseModel


class VotingScore(BaseModel):
    class Meta:
        verbose_name = _('Voting Score')
        verbose_name_plural = _('Voting Scores')

    war = models.ForeignKey(
        to='meme_wars.War',
        on_delete=models.CASCADE,
        verbose_name=_('war'),
        related_name='voting_scores',
    )
    label = models.CharField(
        verbose_name=_('label'),
        max_length=250,
    )

    def __str__(self):
        return self.label

    @property
    def order(self) -> int:
        try:
            return list(self.war.voting_scores.all()).index(self) + 1
        except ValueError:
            pass
