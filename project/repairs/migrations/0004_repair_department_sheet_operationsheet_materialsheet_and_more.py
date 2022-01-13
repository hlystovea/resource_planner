# Generated by Django 4.0.1 on 2022-01-12 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
        ('warehouse', '0003_material_delete_materials_alter_instrument_image'),
        ('repairs', '0003_alter_repair_options_remove_repair_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='repair',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repairs', to='staff.dept', verbose_name='Подразделение'),
        ),
        migrations.CreateModel(
            name='Sheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sheets', to='repairs.object', verbose_name='Оборудование')),
            ],
            options={
                'verbose_name': 'Ресурсная ведомость',
                'verbose_name_plural': 'Ресурсные ведомости',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='OperationSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='Количество')),
                ('operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repairs.operation', verbose_name='Наименование')),
                ('sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operations', to='repairs.sheet')),
            ],
            options={
                'verbose_name': 'Операция',
                'verbose_name_plural': 'Операции',
                'ordering': ('operation__name',),
            },
        ),
        migrations.CreateModel(
            name='MaterialSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='Количество')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.material', verbose_name='Наименование')),
                ('sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='repairs.sheet')),
            ],
            options={
                'verbose_name': 'Материал',
                'verbose_name_plural': 'Материалы',
                'ordering': ('material__name',),
            },
        ),
        migrations.CreateModel(
            name='InstrumentSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.SmallIntegerField(verbose_name='Количество')),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.instrument', verbose_name='Наименование')),
                ('sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instruments', to='repairs.sheet')),
            ],
            options={
                'verbose_name': 'Инструмент',
                'verbose_name_plural': 'Инструменты',
                'ordering': ('instrument__name',),
            },
        ),
        migrations.AddField(
            model_name='repair',
            name='sheet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repairs', to='repairs.sheet', verbose_name='Ресурсная ведомость'),
        ),
    ]