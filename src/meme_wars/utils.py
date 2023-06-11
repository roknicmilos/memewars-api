from decouple import config, undefined
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def get_env_url(env_var: str, default=undefined) -> str:
    url = config(env_var, default=default)

    url_validator = URLValidator()
    try:
        url_validator(url)
    except ValidationError:
        raise ValidationError(
            f'Environment variable "{env_var}" is an invalid URL ("{url}")'
        )

    return url
