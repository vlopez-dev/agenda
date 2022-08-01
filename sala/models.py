from statistics import mode
from django.db import models

# Create your models here.

class Sala(models.Model):
    nombre=models.CharField(max_length=150)
    ubicacion=models.CharField(max_length=50)
    estado=models.BooleanField(null=True)
    reserva_id = models.ForeignKey('reserva.reserva',on_delete=models.CASCADE,blank=True,null=True)
