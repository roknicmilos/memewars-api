from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.common.models import BaseModel
from apps.wars.models import War
from apps.wars.validators import MemeWarPhaseValidator


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
        to='wars.Meme',
        on_delete=models.CASCADE,
        verbose_name=_('meme'),
        related_name='votes',
        validators=[
            MemeWarPhaseValidator(phase_value=War.Phases.SUBMISSION)
        ]
    )
    score = models.IntegerField(
        verbose_name=_('score'),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
    )
    submission_count = models.IntegerField(
        verbose_name=_('total submissions'),
        default=1,
    )

    def __str__(self):
        return f'Vote {self.pk}'

    @property
    def war(self) -> War:
        return self.meme.war
