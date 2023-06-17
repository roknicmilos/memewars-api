from decouple import config, undefined
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db.models import Model
from django.urls import reverse, reverse_lazy, NoReverseMatch

from meme_wars.urls import MAIN_URL_CONF, ADMIN_URL_CONF, API_URL_CONF


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


def reverse_main(
        view_name: str,
        args: tuple = None,
        kwargs: tuple = None,
        current_app: str = None
) -> str:
    return reverse(
        viewname=view_name,
        args=args,
        kwargs=kwargs,
        current_app=current_app,
        urlconf=MAIN_URL_CONF
    )


def reverse_admin(
        view_name: str,
        args: tuple = None,
        kwargs: tuple = None,
        current_app: str = None
) -> str:
    return reverse(
        viewname=view_name,
        args=args,
        kwargs=kwargs,
        current_app=current_app,
        urlconf=ADMIN_URL_CONF
    )


def reverse_api(
        view_name: str,
        args: tuple = None,
        kwargs: tuple = None,
        current_app: str = None
) -> str:
    return reverse(
        viewname=view_name,
        args=args,
        kwargs=kwargs,
        current_app=current_app,
        urlconf=API_URL_CONF
    )


def reverse_lazy_api(
        view_name: str,
        args: tuple = None,
        kwargs: tuple = None,
        current_app: str = None
) -> str:
    return reverse_lazy(
        viewname=view_name,
        args=args,
        kwargs=kwargs,
        current_app=current_app,
        urlconf=API_URL_CONF
    )


def build_absolute_uri(view_name: str, args: tuple = None, kwargs: dict = None) -> str:
    return f'{settings.HOST_URL}{reverse_main(view_name=view_name, args=args, kwargs=kwargs)}'


def build_absolute_admin_uri(view_name: str, args: tuple = None, kwargs: dict = None) -> str:
    return f'{settings.ADMIN_URL}{reverse_admin(view_name=view_name, args=args, kwargs=kwargs)}'


def build_absolute_api_uri(view_name: str, args: tuple = None, kwargs: dict = None) -> str:
    return f'{settings.API_URL}{reverse_api(view_name=view_name, args=args, kwargs=kwargs)}'


def get_model_admin_change_details_url(obj: Model) -> str:
    from django.contrib.contenttypes.models import ContentType
    content_type = ContentType.objects.get_for_model(obj.__class__)
    try:
        view_name = f'admin:{content_type.app_label}_{content_type.model}_change'
        return reverse_admin(view_name=view_name, args=(obj.id,))
    except NoReverseMatch:
        return ''
