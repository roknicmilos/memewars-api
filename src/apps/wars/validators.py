from django.core.validators import BaseValidator
from django.utils.translation import gettext_lazy as _
from apps.wars.models import War


class WarPhaseValidator(BaseValidator):
    code = 'limit_war_phase'

    def __init__(self, war_phase: War.Phases, message=None):
        if war_phase not in War.Phases:
            raise ValueError('Invalid War Phase')

        if not message:
            message = _(f'War must be in "{war_phase.label}" phase in order to add a meme to it')

        super().__init__(war_phase, message)

    def compare(self, a, b):
        return a is not b
