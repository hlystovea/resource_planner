# Generated by Django 4.1 on 2022-08-28 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("repairs", "0001_initial"),
        ("staff", "0001_initial"),
        ("hardware", "0001_initial"),
        ("warehouse", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="sheet",
            name="department",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sheets",
                to="staff.dept",
                verbose_name="Подразделение",
            ),
        ),
        migrations.AddField(
            model_name="repair",
            name="department",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="repairs",
                to="staff.dept",
                verbose_name="Подразделение",
            ),
        ),
        migrations.AddField(
            model_name="repair",
            name="hardware",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="repairs",
                to="hardware.hardware",
                verbose_name="Оборудование",
            ),
        ),
        migrations.AddField(
            model_name="repair",
            name="sheet",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="repairs",
                to="repairs.sheet",
                verbose_name="Ресурсная ведомость",
            ),
        ),
        migrations.AddField(
            model_name="repair",
            name="type_repair",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="repairs",
                to="repairs.typerepair",
                verbose_name="Вид ТО",
            ),
        ),
        migrations.AddField(
            model_name="operationsheet",
            name="operation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="repairs.operation",
                verbose_name="Наименование",
            ),
        ),
        migrations.AddField(
            model_name="operationsheet",
            name="sheet",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="operations",
                to="repairs.sheet",
            ),
        ),
        migrations.AddField(
            model_name="materialsheet",
            name="material",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="warehouse.material",
                verbose_name="Наименование",
            ),
        ),
        migrations.AddField(
            model_name="materialsheet",
            name="sheet",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="materials",
                to="repairs.sheet",
            ),
        ),
        migrations.AddField(
            model_name="instrumentsheet",
            name="instrument",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="warehouse.instrument",
                verbose_name="Наименование",
            ),
        ),
        migrations.AddField(
            model_name="instrumentsheet",
            name="sheet",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="instruments",
                to="repairs.sheet",
            ),
        ),
    ]
