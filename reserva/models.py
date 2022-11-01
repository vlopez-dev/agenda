from datetime import date, timezone
from statistics import mode
import django
from django.db import models

# Create your models here.
class Reserva(models.Model):
    titulo = models.CharField(max_length=50)
    tiempo_inicio = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        default=django.utils.timezone.now,
    )
    tiempo_fin = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        default=django.utils.timezone.now,
    )
    username = models.ForeignKey(
        "auth.user", on_delete=models.CASCADE, blank=True, null=True
    )
    descripcion = models.CharField(max_length=500, blank=True)
    sala_id = models.ForeignKey(
        "sala.sala", on_delete=models.CASCADE, blank=True, null=True, default=1
    )
    invitados = models.EmailField(max_length=254, null=True)

    def add(self):
        self.save

    def __str__(self):
        return self.name
