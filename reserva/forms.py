from pyexpat import model
from django.db.models import fields
from django import forms
from .models import Reserva
from bootstrap_datepicker_plus.widgets import  DateTimePickerInput

class ReservaForm(forms.ModelForm):
    
    class Meta:
        model=Reserva
        fields = ['tiempo_inicio', 'tiempo_fin','usuario_reserva','descripcion','sala_id']
        widgets = {
            'tiempo_inicio': DateTimePickerInput(),
            'tiempo_fin': DateTimePickerInput(),
            
        }
