from django.utils.translation import gettext_lazy as _

from apps.common.validators import BaseArrayValidator


class AsteriskValidator(BaseArrayValidator):
    message = _("The list can't contain other values if asterisk is present in the list")
    code = "asterisk_not_solo"

    def compare(self, a, b):
        return "*" in a and len(a) > 1
