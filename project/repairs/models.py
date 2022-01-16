from django.db import models
from django.utils.translation import gettext_lazy as _


class Object(models.Model):
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
    connection = models.CharField(
        verbose_name=_('Присоединение'),
        max_length=50,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Оборудование')
        verbose_name_plural = _('Оборудование')

    def __str__(self):
        return f'{self.name} ({self.inventory_number})'


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
    object = models.ForeignKey(
        to=Object,
        verbose_name=_('Оборудование'),
        on_delete=models.CASCADE,
        related_name='repairs',
    )
    department = models.ForeignKey(
        to='staff.Dept',
        verbose_name=_('Подразделение'),
        on_delete=models.CASCADE,
        related_name='repairs',
        null=True,
    )
    sheet = models.ForeignKey(
        to=Sheet,
        verbose_name=_('Ресурсная ведомость'),
        on_delete=models.CASCADE,
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
        verbose_name = _('Плановая работа')
        verbose_name_plural = _('Плановые работы')
