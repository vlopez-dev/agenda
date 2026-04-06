from django.contrib import admin
from .models import ConfigEmail

@admin.register(ConfigEmail)
class ConfigEmailAdmin(admin.ModelAdmin):
    list_display = ('host_user', 'email_host', 'host_port', 'use_tls', 'use_ssl')
