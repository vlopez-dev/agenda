from statistics import mode
from django.db import models

# Create your models here.

class Sala(models.Model):
    nombre=models.CharField(max_length=150)
    ubicacion=models.CharField(max_length=50)
    estado=models.BooleanField(null=False,default=False)


    def add(self):
            self.save


    def __str__(self):
            return self.nombre
