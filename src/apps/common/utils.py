from django.db.models import Model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse, NoReverseMatch


def get_model_admin_change_details_url(obj: Model) -> str:
    content_type = ContentType.objects.get_for_model(obj.__class__)
    try:
        return reverse(f'admin:{content_type.app_label}_{content_type.model}_change', args=(obj.id,))
    except NoReverseMatch:
        return ''
