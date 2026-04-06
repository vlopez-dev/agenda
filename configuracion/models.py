from django.db import models

# Create your models here.

class ConfigEmail(models.Model):
    email_host = models.CharField(max_length=100)
    host_user = models.CharField(max_length=100)
    host_password = models.CharField(max_length=100)
    host_port = models.IntegerField(default=587)
    use_tls = models.BooleanField(default=True)
    use_ssl = models.BooleanField(default=False)
    default_from_email = models.EmailField(default='web@vic.uy')

    def __str__(self):
        return f"Configuración: {self.host_user} ({self.email_host})"