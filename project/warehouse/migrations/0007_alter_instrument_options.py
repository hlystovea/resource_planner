# Generated by Django 4.0.1 on 2022-01-14 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0006_alter_material_options_remove_instrument_storage_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instrument',
            options={'ordering': ('name',), 'verbose_name': 'Инструмент/прибор', 'verbose_name_plural': 'Инструмент/приборы'},
        ),
    ]
