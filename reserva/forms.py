from cProfile import label
from pyexpat import model
from django.db.models import fields
from django import forms
from .models import Reserva


class ReservaForm(forms.ModelForm):
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "3", "cols": "5"})
    )

    class Meta:
        model = Reserva
        fields = [
            "tiempo_inicio",
            "tiempo_fin",
            "username",
            "descripcion",
            "sala_id",
            "titulo",
            "invitados",
        ]

        labels = {
            "tiempo_inicio": "Inicio",
            "tiempo_fin": "Fin",
            "username": "usuario",
            "descripcion": "Descripción",
            "sala_id": "Sala",
        }
