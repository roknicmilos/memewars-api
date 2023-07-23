from django.core.validators import BaseValidator
from django.utils.translation import gettext_lazy as _

from apps.common.utils import get_text_choice_by_value
from apps.wars.models import War


class WarPhaseValidator(BaseValidator):
    code = "limit_war_phase"

    def __init__(self, phase_value: str, message=None):
        war_phase = get_text_choice_by_value(value=phase_value, text_choices=War.Phases)

        if not message:
            message = _(f'War must be in "{war_phase.label}" phase')

        super().__init__(war_phase, message)

    def compare(self, a, b):
        if isinstance(a, War):
            return a.phase != b
        return not War.objects.filter(pk=a, phase=b).exists()
