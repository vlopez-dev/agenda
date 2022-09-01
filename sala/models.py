from statistics import mode
from django.db import models
from colorfield.fields import ColorField

# Create your models here.
COLOR_PALETTE = [
        ("#FFFFFF", "white", ),
        ("#000000", "black", ),
    ]
class Sala(models.Model):
    nombre=models.CharField(max_length=150)
    ubicacion=models.CharField(max_length=50)
    color = ColorField(default='#FF0000',samples=COLOR_PALETTE)
    
    
    
    def add(self):
            self.save


    def __str__(self):
            return self.nombre
