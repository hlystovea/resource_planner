# Generated by Django 4.0.1 on 2022-01-16 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0008_storage_qr_code_alter_instrument_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storage',
            name='qr_code',
        ),
    ]