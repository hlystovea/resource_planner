from django.db import models
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

    class Meta:
        ordering = ('name', )
        verbose_name = _('Место хранения')
        verbose_name_plural = _('Места хранения')

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
    inventory_number = models.CharField(
        verbose_name=_('Инв. номер'),
        max_length=50,
        blank=True,
        null=True,
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
    storage = models.ForeignKey(
        to=Storage,
        verbose_name=_('Место хранения'),
        on_delete=models.PROTECT,
        related_name='materials',
        blank=True,
        null=True,
    )
    image = ResizedImageField(
        verbose_name=_('Изображение'),
        upload_to='material/',
        blank=True,
        null=True,
        size=[1280, 720],
        crop=['middle', 'center'],
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Материал')
        verbose_name_plural = _('Материалы')

    def __str__(self):
        return f'{self.name} ({self.inventory_number})'


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
    storage = models.ForeignKey(
        to=Storage,
        verbose_name=_('Место хранения'),
        on_delete=models.PROTECT,
        related_name='instruments',
        blank=True,
        null=True,
    )
    image = ResizedImageField(
        verbose_name=_('Изображение'),
        upload_to='instrument/',
        blank=True,
        null=True,
        size=[1280, 720],
        crop=['middle', 'center'],
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Инструмент/Прибор')
        verbose_name_plural = _('Инструменты/Приборы')

    def __str__(self):
        return f'{self.name} ({self.inventory_number})'
