# Generated by Django 4.0.1 on 2022-02-12 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
                ('abbreviation', models.CharField(max_length=30, verbose_name='Аббревиатура')),
            ],
            options={
                'verbose_name': 'Присоединение',
                'verbose_name_plural': 'Присоединения',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
                ('abbreviation', models.CharField(max_length=30, verbose_name='Аббревиатура')),
            ],
            options={
                'verbose_name': 'Объект диспетчеризации',
                'verbose_name_plural': 'Объекты диспетчеризации',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Hardware',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
                ('inventory_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Инв. номер')),
                ('connection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hardwares', to='hardware.connection', verbose_name='Присоединение')),
                ('facility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hardwares', to='hardware.facility', verbose_name='Объект диспетчеризации')),
            ],
            options={
                'verbose_name': 'Оборудование',
                'verbose_name_plural': 'Оборудование',
                'ordering': ('name',),
            },
        ),
    ]
