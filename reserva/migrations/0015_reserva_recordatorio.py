# Generated by Django 4.1.2 on 2022-11-22 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reserva", "0014_alter_reserva_descripcion"),
    ]

    operations = [
        migrations.AddField(
            model_name="reserva",
            name="recordatorio",
            field=models.BooleanField(default=True),
        ),
    ]
