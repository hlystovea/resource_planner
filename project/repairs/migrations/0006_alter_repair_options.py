# Generated by Django 4.0.1 on 2022-01-13 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repairs', '0005_remove_sheet_object_sheet_department'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='repair',
            options={'ordering': ('start_at',), 'verbose_name': 'Плановая работа', 'verbose_name_plural': 'Плановые работы'},
        ),
    ]