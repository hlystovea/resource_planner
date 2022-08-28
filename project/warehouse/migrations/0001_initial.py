# Generated by Django 4.1 on 2022-08-28 14:20

from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("staff", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Material",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="Наименование")),
                (
                    "measurement_unit",
                    models.CharField(max_length=20, verbose_name="Единица измерения"),
                ),
                (
                    "article_number",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="Артикул"
                    ),
                ),
                (
                    "image",
                    django_resized.forms.ResizedImageField(
                        blank=True,
                        crop=None,
                        force_format="JPEG",
                        keep_meta=True,
                        null=True,
                        quality=75,
                        scale=None,
                        size=[1280, 720],
                        upload_to="material/",
                        verbose_name="Изображение",
                    ),
                ),
            ],
            options={
                "verbose_name": "Список материалов",
                "verbose_name_plural": "Список материалов",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Storage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="Наименование")),
                (
                    "parent_storage",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="storage",
                        to="warehouse.storage",
                        verbose_name="Расположение",
                    ),
                ),
            ],
            options={
                "verbose_name": "Место хранения",
                "verbose_name_plural": "Места хранения",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="MaterialStorage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "inventory_number",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Инв. номер"
                    ),
                ),
                ("amount", models.FloatField(verbose_name="Количество")),
                (
                    "material",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="amount",
                        to="warehouse.material",
                        verbose_name="Материал",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="materials",
                        to="staff.dept",
                        verbose_name="Подразделение",
                    ),
                ),
                (
                    "storage",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="materials",
                        to="warehouse.storage",
                        verbose_name="Место хранения",
                    ),
                ),
            ],
            options={
                "verbose_name": "Материал на хранении",
                "verbose_name_plural": "Материалы на хранении",
                "ordering": ("material",),
            },
        ),
        migrations.CreateModel(
            name="Instrument",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="Наименование")),
                (
                    "inventory_number",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Инв. номер"
                    ),
                ),
                (
                    "serial_number",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Зав. номер"
                    ),
                ),
                (
                    "image",
                    django_resized.forms.ResizedImageField(
                        blank=True,
                        crop=None,
                        force_format="JPEG",
                        keep_meta=True,
                        null=True,
                        quality=75,
                        scale=None,
                        size=[1280, 720],
                        upload_to="instrument/",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="instruments",
                        to="staff.dept",
                        verbose_name="Подразделение",
                    ),
                ),
            ],
            options={
                "verbose_name": "Инструмент/прибор",
                "verbose_name_plural": "Инструмент/приборы",
                "ordering": ("name",),
            },
        ),
    ]
