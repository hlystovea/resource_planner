# Generated by Django 4.2.2 on 2024-06-04 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0006_remove_componentstorage_owner_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='last_verification',
            field=models.DateField(blank=True, null=True, verbose_name='Дата последней проверки'),
        ),
        migrations.AddField(
            model_name='instrument',
            name='verification_period',
            field=models.IntegerField(blank=True, null=True, verbose_name='Период проверки (месяцев)'),
        ),
    ]
