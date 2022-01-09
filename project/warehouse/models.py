from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField


class Materials(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name=_('Единица измерения'),
        max_length=20,
    )
    article_number = models.CharField(
        verbose_name=_('Артикул'),
        max_length=30,
        blank=True,
        null=True,
    )
    turnover = models.PositiveSmallIntegerField(
        verbose_name=_('Кол-во применений'),
        default=1,
    )
    image = ResizedImageField(
        verbose_name=_('Изображение'),
        upload_to='materials/',
        blank=True,
        null=True,
        size=[1280, 720],
        crop=['middle', 'center'],
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Материал')
        verbose_name_plural = _('Материалы')


class Instrument(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
    )
    inventory_number = models.CharField(
        verbose_name=_('Инв. номер'),
        max_length=50,
        blank=True,
        null=True,
    )
    serial_number = models.CharField(
        verbose_name=_('Зав. номер'),
        max_length=50,
        blank=True,
        null=True,
    )
    image = ResizedImageField(
        verbose_name=_('Изображение'),
        upload_to='materials/',
        blank=True,
        null=True,
        size=[1280, 720],
        crop=['middle', 'center'],
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Инструмент')
        verbose_name_plural = _('Инструменты')
