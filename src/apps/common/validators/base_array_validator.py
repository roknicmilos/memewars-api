from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import BaseValidator
from django.utils.translation import gettext_lazy as _


class BaseArrayValidator(BaseValidator):
    def __init__(self):
        super().__init__(limit_value=None, message=None)

    def clean(self, x):
        if not isinstance(x, list):
            raise DjangoValidationError(_("This field does not store a list"))
        return x
