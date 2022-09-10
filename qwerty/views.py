from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['links'] = [
            {'label': _('Meme Wars App'), 'url': 'https://memewars.qwertymania.com/'},
            {'label': _('Meme Wars Back Office'), 'url': 'https://admin.memewars.qwertymania.com/admin/'},
        ]
        return context
