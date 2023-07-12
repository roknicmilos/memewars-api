from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WarsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.wars"
    verbose_name = _("Meme Wars")
