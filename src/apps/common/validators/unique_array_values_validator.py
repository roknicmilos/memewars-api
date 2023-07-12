from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from apps.common.validators import BaseArrayValidator


@deconstructible
class UniqueArrayValuesValidator(BaseArrayValidator):
    message = _("The list contains duplicate values")
    code = "duplicate_array_values"

    def compare(self, a, b):
        return len(a) > len(set(a))
