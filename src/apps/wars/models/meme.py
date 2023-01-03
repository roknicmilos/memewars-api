from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from apps.common.models import BaseModel


class Meme(BaseModel):
    class Meta:
        verbose_name = _('Meme')
        verbose_name_plural = _('Memes')

    war = models.ForeignKey(
        verbose_name=_('war'),
        to='wars.War',
        on_delete=models.PROTECT,
        related_name='memes',
    )
    user = models.ForeignKey(
        verbose_name=_('user'),
        to='users.User',
        on_delete=models.PROTECT,
        related_name='memes',
    )
    image = models.ImageField(
        verbose_name=_('image'),
        upload_to='memes',
    )

    def __str__(self):
        return self.image.name

    @property
    def total_score(self) -> float:
        scores_sum = self.votes.aggregate(Sum('score')).get('score__sum') or 0
        return round(scores_sum / self.votes.count(), 2)

    @property
    def vote_count(self) -> int:
        return self.votes.count()