from pyexpat import model
from django.db import models

# Create your models here.



class Configuracion(models.Model):
    email_host=models.CharField(max_length=50)
    host_user = models.CharField(max_length=50)
    host_password = models.CharField(max_length=50)
    host_port = models.CharField(max_length=50)