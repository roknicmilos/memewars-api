from django.db import models
from django.db.models import Sum
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
    def total_score(self) -> float:
        scores_sum = self.votes.aggregate(Sum('score')).get('score__sum') or 0
        return round(scores_sum / self.votes.count(), 2)

    @property
    def vote_count(self) -> int:
        return self.votes.count()
