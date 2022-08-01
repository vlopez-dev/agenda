# Generated by Django 4.0.6 on 2022-07-29 01:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reserva', '0002_reserva_descripcion_reserva_tiempo_reserva_and_more'),
        ('sala', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sala',
            name='sala_id',
        ),
        migrations.AddField(
            model_name='sala',
            name='reserva_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reserva.reserva'),
        ),
    ]
