# Generated by Django 4.1 on 2022-08-28 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="InstrumentSheet",
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
                ("amount", models.SmallIntegerField(verbose_name="Количество")),
            ],
            options={
                "verbose_name": "Инструмент",
                "verbose_name_plural": "Инструменты",
                "ordering": ("instrument__name",),
            },
        ),
        migrations.CreateModel(
            name="MaterialSheet",
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
                ("amount", models.FloatField(verbose_name="Количество")),
            ],
            options={
                "verbose_name": "Материал",
                "verbose_name_plural": "Материалы",
                "ordering": ("material__name",),
            },
        ),
        migrations.CreateModel(
            name="Operation",
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
                    "man_hours",
                    models.FloatField(default=0, verbose_name="Трудозатраты чел/ч"),
                ),
            ],
            options={
                "verbose_name": "Воздействие",
                "verbose_name_plural": "Воздействия",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="OperationSheet",
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
                ("amount", models.FloatField(verbose_name="Количество")),
            ],
            options={
                "verbose_name": "Операция",
                "verbose_name_plural": "Операции",
                "ordering": ("operation__name",),
            },
        ),
        migrations.CreateModel(
            name="Repair",
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
                ("start_at", models.DateTimeField(verbose_name="Время начала")),
                ("end_at", models.DateTimeField(verbose_name="Время окончания")),
            ],
            options={
                "verbose_name": "Ремонт",
                "verbose_name_plural": "Ремонты",
                "ordering": ("start_at",),
            },
        ),
        migrations.CreateModel(
            name="Sheet",
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
            ],
            options={
                "verbose_name": "Ресурсная ведомость",
                "verbose_name_plural": "Ресурсные ведомости",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="TypeRepair",
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
                    "abbreviation",
                    models.CharField(max_length=10, verbose_name="Аббревиатура"),
                ),
            ],
            options={
                "verbose_name": "Вид ТО",
                "verbose_name_plural": "Виды ТО",
                "ordering": ("abbreviation",),
            },
        ),
    ]
