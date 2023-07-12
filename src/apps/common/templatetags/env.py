from decouple import config
from django.template.defaulttags import register


@register.filter
def env(key, default: str = "") -> str:
    return config(key, default=default)


@register.filter
def bool_env(key, default: bool = False) -> bool:
    return config(key, default=default, cast=bool)
