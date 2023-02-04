from django import forms

from apps.wars.admin.widgets import MemeAdminWidget


class MemeAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget = MemeAdminWidget()
