from django.db import models
from django.utils.translation import gettext_lazy as _


class Object(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=300,
    )
    inventory_number = models.CharField(
        verbose_name=_('Инв. номер'),
        max_length=50,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Объект ОС')
        verbose_name_plural = _('Объекты ОС')

    def __str__(self):
        return f'{self.name} ({self.inventory_number})'


class Repair(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
    )
    object = models.ForeignKey(
        to=Object,
        verbose_name=_('Оборудование'),
        on_delete=models.CASCADE,
        related_name='repairs',
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        ordering = ('start_time', )
        verbose_name = _('Ремонт')
        verbose_name_plural = _('Ремонты')


class Operation(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
    )
    man_hours = models.FloatField(
        verbose_name=_('Трудозатраты чел/ч'),
        default=0,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Операция')
        verbose_name_plural = _('Операции')

    def __str__(self):
        return f'{self.name} ({self.man_hours})'
