# Generated by Django 4.0.1 on 2022-01-14 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_alter_dept_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dept',
            name='abbreviation',
            field=models.CharField(max_length=30, verbose_name='Аббревиатура'),
        ),
    ]