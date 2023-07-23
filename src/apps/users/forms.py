from django import forms

from apps.users.models import UserSettings


class UserSettingsAdminForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        widgets = {
            "allowed_email_domains": forms.Textarea(attrs={"cols": 100}),
            "allowed_emails": forms.Textarea(attrs={"cols": 100}),
        }
        fields = "__all__"
