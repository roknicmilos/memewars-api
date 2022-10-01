from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from apps.common.models import BaseModel


class War(BaseModel):
    class Meta:
        verbose_name = _('War')
        verbose_name_plural = _('Wars')

    class Phases(models.TextChoices):
        PREPARATION = 'preparation', _('preparation')
        SUBMISSION = 'submission', _('submission')
        VOTING = 'voting', _('voting')
        FINISHED = 'finished', _('finished')

    name = models.CharField(
        verbose_name=_('name'),
        max_length=250,
    )
    phase = models.CharField(
        verbose_name=_('phase'),
        max_length=12,
        choices=Phases.choices,
        default=Phases.PREPARATION,
    )

    def __str__(self):
        return self.name

    @property
    def memes(self) -> QuerySet:
        from apps.meme_wars.models import Meme
        return Meme.objects.filter(enlistment__in=self.enlistments.all())

    @property
    def votes(self) -> QuerySet:
        from apps.meme_wars.models import Vote
        return Vote.objects.filter(meme__enlistment__war=self)

    @property
    def voter_count(self) -> int:
        return self.votes.distinct('user').count()
