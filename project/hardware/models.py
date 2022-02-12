from django.db import models
from django.utils.translation import gettext_lazy as _


class Connection(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
    )
    abbreviation = models.CharField(
        verbose_name=_('Аббревиатура'),
        max_length=30,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Присоединение')
        verbose_name_plural = _('Присоединения')

    def __str__(self):
        return self.abbreviation


class Facility(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
    )
    abbreviation = models.CharField(
        verbose_name=_('Аббревиатура'),
        max_length=30,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Объект диспетчеризации')
        verbose_name_plural = _('Объекты диспетчеризации')

    def __str__(self):
        return self.abbreviation


class Hardware(models.Model):
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
    facility = models.ForeignKey(
        to='hardware.Facility',
        verbose_name=_('Объект диспетчеризации'),
        on_delete=models.SET_NULL,
        related_name='hardwares',
        blank=True,
        null=True,
    )
    connection = models.ForeignKey(
        to='hardware.Connection',
        verbose_name=_('Присоединение'),
        on_delete=models.SET_NULL,
        related_name='hardwares',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Оборудование')
        verbose_name_plural = _('Оборудование')

    def __str__(self):
        return f'{self.name} ({self.inventory_number})'
