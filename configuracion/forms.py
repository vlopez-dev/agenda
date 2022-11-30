from django.db.models import fields
from django import forms
from .models import ConfigEmail


class ConfigEmailForm(forms.ModelForm):
    class Meta:
        model=ConfigEmail
        fields='__all__'