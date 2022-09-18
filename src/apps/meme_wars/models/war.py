from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from apps.common.models import BaseModel


class War(BaseModel):
    class Meta:
        verbose_name = _('War')
        verbose_name_plural = _('Wars')

    name = models.CharField(
        verbose_name=_('name'),
        max_length=250,
    )
    has_ended = models.BooleanField(
        verbose_name=_('has ended'),
        default=False,
        help_text=_(
            'If the war has ended, it will not accept new enlistments or votes. '
            'Results of the war will be available on the API only after the war ends.'
        )
    )
    is_published = models.BooleanField(
        verbose_name=_('is published'),
        default=False,
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
    def enlistment_count(self) -> int:
        return self.enlistments.count()

    @property
    def meme_count(self) -> int:
        return self.memes.count()

    @property
    def voter_count(self) -> int:
        return self.votes.distinct('user').count()

    @property
    def vote_count(self) -> int:
        return self.votes.count()
