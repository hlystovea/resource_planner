# Generated by Django 4.0.1 on 2022-01-13 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_alter_dept_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dept',
            options={'ordering': ('name',), 'verbose_name': 'Участок/группа/отдел', 'verbose_name_plural': 'Участки/группы/отделы'},
        ),
    ]
