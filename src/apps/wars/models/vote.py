from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.wars.models import War
from apps.wars.validators import MemeWarPhaseValidator


class Vote(BaseModel):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        related_name="votes",
    )
    meme = models.ForeignKey(
        to="wars.Meme",
        on_delete=models.CASCADE,
        verbose_name=_("meme"),
        related_name="votes",
        validators=[MemeWarPhaseValidator(phase_value=War.Phases.VOTING)],
    )
    score = models.IntegerField(
        verbose_name=_("score"),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
    )
    submission_count = models.IntegerField(
        verbose_name=_("total submissions"),
        default=1,
    )

    class Meta:
        verbose_name = _("Vote")
        verbose_name_plural = _("Votes")
        constraints = [models.UniqueConstraint(fields=["user", "meme"], name="unique_user_meme")]

    def __str__(self):
        return f"Vote {self.pk}"

    @property
    def war(self) -> War:
        return self.meme.war
