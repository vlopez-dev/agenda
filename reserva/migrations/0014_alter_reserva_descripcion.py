# Generated by Django 4.1.2 on 2022-10-31 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reserva", "0013_alter_reserva_sala_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reserva",
            name="descripcion",
            field=models.CharField(blank=True, max_length=500),
        ),
    ]