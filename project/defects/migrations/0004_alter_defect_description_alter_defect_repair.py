# Generated by Django 4.1 on 2022-11-01 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('defects', '0003_remove_defect_cabinet_remove_defect_hardware'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defect',
            name='description',
            field=models.CharField(max_length=1500, verbose_name='Описание дефекта'),
        ),
        migrations.AlterField(
            model_name='defect',
            name='repair',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Выполненные мероприятия'),
        ),
    ]
