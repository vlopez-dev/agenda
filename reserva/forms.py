from pyexpat import model
from django.db.models import fields
from django import forms
from .models import Reserva


class ReservaForm(forms.ModelForm):
    
    class Meta:
        model=Reserva
        fields='__all__'