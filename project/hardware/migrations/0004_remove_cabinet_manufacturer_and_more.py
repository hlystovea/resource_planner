# Generated by Django 4.2.1 on 2023-05-17 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0003_remove_group_abbreviation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cabinet',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='component',
            name='manufacturer',
        ),
    ]
