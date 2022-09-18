from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.conf import settings


# TODO: move to "core" app
class IndexView(TemplateView):
    template_name = '../templates/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['links'] = [
            {'label': _('Meme Wars App'), 'url': settings.MEME_WARS_APP_URL},
        ]
        return context
