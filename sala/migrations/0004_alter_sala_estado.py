# Generated by Django 4.0.6 on 2022-08-10 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sala', '0003_remove_sala_reserva_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sala',
            name='estado',
            field=models.BooleanField(default=False),
        ),
    ]
