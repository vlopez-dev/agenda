# Generated by Django 4.1 on 2022-08-29 16:34

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sala', '0005_remove_sala_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='sala',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=18, samples=None),
        ),
    ]
