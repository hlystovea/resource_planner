from django.db import models
from django.utils.translation import gettext_lazy as _


class Sheet(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
    )
    object = models.ForeignKey(
        to='repairs.Object',
        verbose_name=_('Оборудование'),
        on_delete=models.CASCADE,
        related_name='sheets',
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Ресурсная ведомость')
        verbose_name_plural = _('Ресурсные ведомости')


class OperationSheet(models.Model):
    sheet = models.ForeignKey(
        to=Sheet,
        on_delete=models.CASCADE,
        related_name='operations',
    )
    operation = models.ForeignKey(
        to='repairs.Operation',
        verbose_name=_('Наименование'),
        on_delete=models.CASCADE,
    )
    amount = models.FloatField(
        verbose_name=_('Количество'),
    )

    class Meta:
        ordering = ('operation__name', )
        verbose_name = _('Операция')
        verbose_name_plural = _('Операции')


class InstrumentSheet(models.Model):
    sheet = models.ForeignKey(
        to=Sheet,
        on_delete=models.CASCADE,
        related_name='instruments',
    )
    instrument = models.ForeignKey(
        to='warehouse.Instrument',
        verbose_name=_('Наименование'),
        on_delete=models.CASCADE,
    )
    amount = models.SmallIntegerField(
        verbose_name=_('Количество'),
    )

    class Meta:
        ordering = ('instrument__name', )
        verbose_name = _('Инструмент')
        verbose_name_plural = _('Инструменты')


class MaterialSheet(models.Model):
    sheet = models.ForeignKey(
        to=Sheet,
        on_delete=models.CASCADE,
        related_name='materials',
    )
    material = models.ForeignKey(
        to='warehouse.Material',
        verbose_name=_('Наименование'),
        on_delete=models.CASCADE,
    )
    amount = models.FloatField(
        verbose_name=_('Количество'),
    )

    class Meta:
        ordering = ('material__name', )
        verbose_name = _('Материал')
        verbose_name_plural = _('Материалы')
