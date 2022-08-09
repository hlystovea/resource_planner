from django.db import models
from django.utils.translation import gettext_lazy as _


class TypeRepair(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
    )
    abbreviation = models.CharField(
        verbose_name=_('Аббревиатура'),
        max_length=10,
    )

    class Meta:
        ordering = ('abbreviation', )
        verbose_name = _('Вид ТО')
        verbose_name_plural = _('Виды ТО')

    def __str__(self):
        return self.abbreviation


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
        verbose_name = _('Воздействие')
        verbose_name_plural = _('Воздействия')

    def __str__(self):
        return f'{self.name} ({self.man_hours})'


class Sheet(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
    )
    department = models.ForeignKey(
        to='staff.Dept',
        verbose_name=_('Подразделение'),
        on_delete=models.CASCADE,
        related_name='sheets',
        null=True,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Ресурсная ведомость')
        verbose_name_plural = _('Ресурсные ведомости')

    def __str__(self):
        return self.name


class OperationSheet(models.Model):
    sheet = models.ForeignKey(
        to=Sheet,
        on_delete=models.CASCADE,
        related_name='operations',
    )
    operation = models.ForeignKey(
        to=Operation,
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


class Repair(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
    )
    hardware = models.ForeignKey(
        to='hardware.Hardware',
        verbose_name=_('Оборудование'),
        on_delete=models.CASCADE,
        related_name='repairs',
    )
    type_repair = models.ForeignKey(
        to=TypeRepair,
        verbose_name=_('Вид ТО'),
        on_delete=models.SET_NULL,
        related_name='repairs',
        null=True,
    )
    department = models.ForeignKey(
        to='staff.Dept',
        verbose_name=_('Подразделение'),
        on_delete=models.SET_NULL,
        related_name='repairs',
        null=True,
    )
    sheet = models.ForeignKey(
        to=Sheet,
        verbose_name=_('Ресурсная ведомость'),
        on_delete=models.SET_NULL,
        related_name='repairs',
        blank=True,
        null=True,
    )
    start_at = models.DateTimeField(
        verbose_name=_('Время начала'),
    )
    end_at = models.DateTimeField(
        verbose_name=_('Время окончания'),
    )

    class Meta:
        ordering = ('start_at', )
        verbose_name = _('Ремонт')
        verbose_name_plural = _('Ремонты')
