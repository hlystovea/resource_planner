# Generated by Django 4.1 on 2022-11-18 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hardware', '0002_group_alter_hardware_connection_hardware_group'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Условие обнаружения',
                'verbose_name_plural': 'Условия обнаружения',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Effect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Последствие дефекта',
                'verbose_name_plural': 'Последствия дефекта',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Признак дефекта',
                'verbose_name_plural': 'Признаки дефекта',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='OrganizationalReason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Наименование')),
                ('is_dependent', models.BooleanField(default=False, verbose_name='Зависит от внешних условий')),
            ],
            options={
                'verbose_name': 'Организационная причина',
                'verbose_name_plural': 'Организационные причины',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='TechnicalReason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Наименование')),
                ('is_dependent', models.BooleanField(default=False, verbose_name='Зависит от внешних условий')),
            ],
            options={
                'verbose_name': 'Техническая причина',
                'verbose_name_plural': 'Технические причины',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Defect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата обнаружения')),
                ('description', models.CharField(max_length=1500, verbose_name='Описание дефекта')),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=75, scale=None, size=[1280, 720], upload_to='defects/', verbose_name='Фото')),
                ('repair', models.TextField(blank=True, max_length=500, null=True, verbose_name='Выполненные мероприятия')),
                ('repair_date', models.DateField(blank=True, null=True, verbose_name='Дата устранения')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='defects', to='hardware.component', verbose_name='Комплектующее')),
                ('condition', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='defects', to='defects.condition', verbose_name='Условие обнаружения')),
                ('effects', models.ManyToManyField(related_name='defects', to='defects.effect', verbose_name='Последствия дефекта')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='defects', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник обнаруживший дефект')),
                ('features', models.ManyToManyField(related_name='defects', to='defects.feature', verbose_name='Признаки дефекта')),
                ('organizational_reasons', models.ManyToManyField(blank=True, related_name='defects', to='defects.organizationalreason', verbose_name='Организационные причины')),
                ('technical_reasons', models.ManyToManyField(blank=True, related_name='defects', to='defects.technicalreason', verbose_name='Технические причины дефекта')),
            ],
            options={
                'verbose_name': 'Дефект',
                'verbose_name_plural': 'Дефекты',
                'ordering': ('-date',),
            },
        ),
    ]
