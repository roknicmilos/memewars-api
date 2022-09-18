from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import User
from apps.common.models import BaseModel
from apps.meme_wars.models import War


class Meme(BaseModel):
    class Meta:
        verbose_name = _('Meme')
        verbose_name_plural = _('Memes')

    enlistment = models.ForeignKey(
        to='meme_wars.Enlistment',
        on_delete=models.CASCADE,
        verbose_name=_('enlistment'),
        related_name='memes',
    )
    image = models.ImageField(
        verbose_name=_('image'),
        upload_to='memes',
    )

    def __str__(self):
        return self.image.name

    @property
    def war(self) -> War:
        return self.enlistment.war

    @property
    def user(self) -> User:
        return self.enlistment.user

    @property
    def scored_value(self) -> float:
        votes_with_scores = self.votes.filter(score__isnull=False).select_related('score')
        if votes_with_scores.exists():
            score_sum = sum([vote.score.order for vote in votes_with_scores])
            return round(score_sum / votes_with_scores.count(), 2)

        return 0

    @property
    def vote_count(self) -> int:
        return self.votes.count()
