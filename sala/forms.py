from pyexpat import model
from django.db.models import fields
from django import forms
from .models import Sala


class SalaForm(forms.ModelForm):
    
    class Meta:
        model=Sala
        fields='__all__'