from decouple import config, undefined
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db.models import Model
from django.urls import NoReverseMatch, reverse


def get_env_url(env_var: str, default=undefined) -> str:
    url = config(env_var, default=default)

    url_validator = URLValidator()
    try:
        url_validator(url)
    except ValidationError:
        raise ValidationError(f'Environment variable "{env_var}" is an invalid URL ("{url}")')

    return url


def build_absolute_uri(view_name: str, args: tuple = None, kwargs: dict = None) -> str:
    return f"{settings.HOST_URL}{reverse(viewname=view_name, args=args, kwargs=kwargs)}"


def get_model_admin_change_details_url(obj: Model) -> str:
    from django.contrib.contenttypes.models import ContentType

    content_type = ContentType.objects.get_for_model(obj.__class__)
    try:
        view_name = f"admin:{content_type.app_label}_{content_type.model}_change"
        return reverse(viewname=view_name, args=(obj.id,))
    except NoReverseMatch:
        return ""
