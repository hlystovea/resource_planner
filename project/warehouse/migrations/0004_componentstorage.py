# Generated by Django 4.2.1 on 2023-09-05 02:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0008_alter_component_name'),
        ('staff', '0001_initial'),
        ('warehouse', '0003_alter_materialstorage_material_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComponentStorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inventory_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Инв. номер')),
                ('amount', models.PositiveSmallIntegerField(verbose_name='Количество')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amount', to='hardware.component', verbose_name='Запчасть')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='components', to='staff.dept', verbose_name='Подразделение')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='warehouse.storage', verbose_name='Место хранения')),
            ],
            options={
                'verbose_name': 'Запчасти на хранении',
                'verbose_name_plural': 'Запчасти на хранении',
                'ordering': ('component',),
            },
        ),
    ]
