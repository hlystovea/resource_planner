# Generated by Django 5.1.1 on 2024-10-17 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0014_alter_part_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='hardware',
            name='abbreviation',
            field=models.CharField(max_length=30, null=True, verbose_name='Аббревиатура'),
        ),
    ]