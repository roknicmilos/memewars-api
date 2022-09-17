from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.conf import settings


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['links'] = [
            {'label': _('Meme Wars App'), 'url': settings.MEME_WARS_FE_URL},
            {'label': _('Meme Wars Back Office'), 'url': settings.MEME_WARS_BE_URL},
        ]
        return context
