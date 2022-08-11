from datetime import date, timezone
import django
from django.db import models

# Create your models here.
class Reserva(models.Model):
    tiempo_inicio=models.DateTimeField( auto_now=False, auto_now_add=False,blank=True,default=django.utils.timezone.now)
    tiempo_fin=models.DateTimeField( auto_now=False, auto_now_add=False,blank=True,default=django.utils.timezone.now)
    usuario_reserva=models.CharField(max_length=50,blank=True)
    descripcion = models.CharField(max_length=150,blank=True)
    sala_id = models.ForeignKey('sala.sala',on_delete=models.CASCADE,blank=True,null=True)




    def add(self):
            self.save


    def __str__(self):
            return self.sala_id
