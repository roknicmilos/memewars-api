from rest_framework.exceptions import ValidationError as APIValidationError
from rest_framework.settings import api_settings


class NonFieldAPIValidationError(APIValidationError):
    def __init__(self, message: str, code: str = None):
        super().__init__(detail={api_settings.NON_FIELD_ERRORS_KEY: [message]}, code=code)
