from django import forms

from apps.wars.admin.widgets import MemeImageAdminWidget


class MemeAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):  # pragma: no cover (don't know how to instantiate the form)
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["image"].widget = MemeImageAdminWidget()
