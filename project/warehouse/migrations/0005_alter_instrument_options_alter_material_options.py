# Generated by Django 4.0.1 on 2022-01-14 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0004_alter_instrument_options_storage_instrument_storage_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instrument',
            options={'ordering': ('name',), 'verbose_name': 'ЗИП', 'verbose_name_plural': 'ЗИП'},
        ),
        migrations.AlterModelOptions(
            name='material',
            options={'ordering': ('name',), 'verbose_name': 'Расходный материал', 'verbose_name_plural': 'Расходные материалы'},
        ),
    ]
