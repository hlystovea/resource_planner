# Generated by Django 4.2.1 on 2024-01-24 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
        ('warehouse', '0004_componentstorage'),
    ]

    operations = [
        migrations.AddField(
            model_name='storage',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='storage', to='staff.dept', verbose_name='Подразделение'),
        ),
    ]
