from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.common.utils import FilePath, compress_image_file
from apps.wars.models import War
from apps.wars.validators import WarPhaseValidator


class Meme(BaseModel):
    class ApprovalStatuses(models.TextChoices):
        PENDING = "pending", _("Pending")
        REJECTED = "rejected", _("Rejected")
        APPROVED = "approved", _("Approved")

    war = models.ForeignKey(
        verbose_name=_("war"),
        to="wars.War",
        on_delete=models.PROTECT,
        related_name="memes",
        validators=[
            WarPhaseValidator(phase_value=War.Phases.SUBMISSION),
        ],
    )
    user = models.ForeignKey(
        verbose_name=_("user"),
        to="users.User",
        on_delete=models.PROTECT,
        related_name="memes",
    )
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to=FilePath("wars/meme/"),
    )
    approval_status = models.CharField(
        verbose_name=_("approval status"),
        max_length=10,
        choices=ApprovalStatuses.choices,
        default=ApprovalStatuses.PENDING,
    )

    class Meta:
        verbose_name = _("Meme")
        verbose_name_plural = _("Memes")

    def __str__(self):
        return f"{self.image.name} ({self.pk})"

    @property
    def total_score(self) -> float:
        if not self.votes.exists():
            return 0

        scores_sum = self.votes.aggregate(Sum("score")).get("score__sum")
        return round(scores_sum / self.votes.count(), 2)

    @property
    def vote_count(self) -> int:
        return self.votes.count()

    def save(self, **kwargs):
        self.clean()
        if self.image and (not self.original or self.image != self.original.image):
            self.image = compress_image_file(image=self.image)
        super().save(**kwargs)

    def clean(self):
        super().clean()
        if not self.pk and self.user.memes.count() >= self.war.meme_upload_limit:
            raise DjangoValidationError(
                message=_("This user already reached Meme upload limit in this war."), code="meme_upload_limit_reached"
            )
