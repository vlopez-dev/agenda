from django.contrib import admin
from django.contrib.auth.models import Group, Permission

from .models import Reserva

admin.site.register(Reserva)

admin.site.unregister(Group)
admin.site.register(Group)
admin.site.register(Permission)
# Register your models here.
