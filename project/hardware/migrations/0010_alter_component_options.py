# Generated by Django 4.2.1 on 2023-09-07 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0009_alter_component_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='component',
            options={'ordering': ('manufacturer', 'name'), 'verbose_name': 'Компонент / запчасть', 'verbose_name_plural': 'Компоненты / запчасти'},
        ),
    ]