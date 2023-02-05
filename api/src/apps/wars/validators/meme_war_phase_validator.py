from django.core.validators import BaseValidator
from django.utils.translation import gettext_lazy as _
from apps.common.utils import get_text_choice_by_value


class MemeWarPhaseValidator(BaseValidator):
    code = 'limit_meme_war_phase'

    def __init__(self, phase_value: str, message=None):
        from apps.wars.models import War
        war_phase = get_text_choice_by_value(value=phase_value, text_choices=War.Phases)

        if not message:
            message = _(f'Meme must be in a war that is in "{War.Phases.SUBMISSION}" phase')

        super().__init__(war_phase, message)

    def compare(self, a, b):
        from apps.wars.models import Meme, War
        return not Meme.objects.filter(pk=a, war__phase=War.Phases.SUBMISSION).exclude()
