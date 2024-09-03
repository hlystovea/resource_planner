from dateutil.relativedelta import relativedelta as rd

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField


class Storage(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
    )
    parent_storage = models.ForeignKey(
        to='warehouse.Storage',
        verbose_name=_('Расположение'),
        on_delete=models.PROTECT,
        related_name='storage',
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        to='staff.Dept',
        verbose_name=_('Подразделение'),
        on_delete=models.SET_NULL,
        related_name='storage',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Место хранения')
        verbose_name_plural = _('Места хранения')

    def get_absolute_url(self):
        return reverse('warehouse:storage-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.name}'


class Material(models.Model):
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
    image = ResizedImageField(
        verbose_name=_('Изображение'),
        upload_to='material/',
        blank=True,
        null=True,
        size=[1280, 720],
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Список материалов')
        verbose_name_plural = _('Список материалов')

    def get_absolute_url(self):
        return reverse('warehouse:material-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return (f'{self.name}, {self.measurement_unit} '
                f'{(self.article_number) if self.article_number else ""}')


class MaterialStorage(models.Model):
    material = models.ForeignKey(
        to=Material,
        verbose_name=_('Материал'),
        on_delete=models.CASCADE,
        related_name='amount',
    )
    inventory_number = models.CharField(
        verbose_name=_('Инв. номер'),
        max_length=50,
        blank=True,
        null=True,
    )
    amount = models.FloatField(
        verbose_name=_('Количество'),
        validators=[
            MinValueValidator(0),
        ]
    )
    storage = models.ForeignKey(
        to=Storage,
        verbose_name=_('Место хранения'),
        on_delete=models.CASCADE,
        related_name='materials',
    )

    class Meta:
        ordering = ('material', )
        verbose_name = _('Материал на хранении')
        verbose_name_plural = _('Материалы на хранении')

    def __str__(self):
        return f'{self.material.name}, {self.material.measurement_unit}'


class Instrument(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
    )
    type = models.CharField(
        verbose_name=_('Тип'),
        max_length=50,
        blank=True,
        null=True,
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
    owner = models.ForeignKey(
        to='staff.Dept',
        verbose_name=_('Подразделение'),
        on_delete=models.SET_NULL,
        related_name='instruments',
        null=True,
    )
    image = ResizedImageField(
        verbose_name=_('Изображение'),
        upload_to='instrument/',
        blank=True,
        null=True,
        size=[1280, 720],
    )
    last_verification = models.DateField(
        verbose_name=_('Дата последней проверки'),
        null=True,
        blank=True,
    )
    verification_period = models.PositiveSmallIntegerField(
        verbose_name=_('Период проверки (месяцев)'),
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Инструмент/прибор')
        verbose_name_plural = _('Инструмент/приборы')

    @property
    def next_verification(self):
        if not (self.last_verification and self.verification_period):
            return None
        return self.last_verification + rd(months=self.verification_period)

    def get_absolute_url(self):
        return reverse('warehouse:instrument-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.name} ({self.inventory_number})'


class ComponentStorage(models.Model):
    component = models.ForeignKey(
        to='hardware.Component',
        verbose_name=_('Запчасть'),
        on_delete=models.CASCADE,
        related_name='amount',
    )
    inventory_number = models.CharField(
        verbose_name=_('Инв. номер'),
        max_length=50,
        blank=True,
        null=True,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name=_('Количество'),
    )
    storage = models.ForeignKey(
        to=Storage,
        verbose_name=_('Место хранения'),
        on_delete=models.CASCADE,
        related_name='components',
    )

    class Meta:
        ordering = ('component', )
        verbose_name = _('Запчасти на хранении')
        verbose_name_plural = _('Запчасти на хранении')

    def __str__(self):
        return f'{self.component.name}, {self.component.type}'
