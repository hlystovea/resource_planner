# Generated by Django 4.2.2 on 2024-07-09 01:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_position_employee_position'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ('last_name',), 'verbose_name': 'Сотрудник', 'verbose_name_plural': 'Сотрудники'},
        ),
    ]
