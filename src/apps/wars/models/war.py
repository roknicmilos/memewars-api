from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class War(BaseModel):
    class Phases(models.TextChoices):
        PREPARATION = "preparation", _("Preparation")
        SUBMISSION = "submission", _("Submission")
        VOTING = "voting", _("Voting")
        FINISHED = "finished", _("Finished")

    name = models.CharField(
        verbose_name=_("name"),
        max_length=250,
    )
    phase = models.CharField(
        verbose_name=_("phase"),
        max_length=12,
        choices=Phases.choices,
        default=Phases.PREPARATION,
    )
    requires_meme_approval = models.BooleanField(
        verbose_name=_("requires meme approval"),
        default=False,
    )
    meme_upload_limit = models.SmallIntegerField(
        verbose_name=_("meme upload limit"),
        default=20,
        help_text=_("Maximum number of memes that one user can upload"),
    )

    class Meta:
        verbose_name = _("War")
        verbose_name_plural = _("Wars")

    def __str__(self):
        return self.name

    @property
    def votes(self) -> QuerySet:
        from apps.wars.models import Vote

        return Vote.objects.filter(meme__war=self)

    @property
    def voter_count(self) -> int:
        return self.votes.distinct("user").count()

    @property
    def vote_count(self) -> int:
        return self.votes.count()

    @property
    def meme_count(self) -> int:
        return self.memes.count()
