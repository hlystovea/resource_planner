from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField


class Defect(models.Model):
    date = models.DateField(
        verbose_name=_('Дата обнаружения')
    )
    hardware = models.ForeignKey(
        to='hardware.Hardware',
        verbose_name=_('Оборудование'),
        on_delete=models.CASCADE,
        related_name='defects'
    )
    employee = models.ForeignKey(
        to='staff.Staff',
        verbose_name=_('Сотрудник обнаруживший дефект'),
        on_delete=models.PROTECT,
        related_name='defects'
    )
    description = models.TextField(
        verbose_name=_('Описание дефекта'),
        max_length=1500,
    )
    image = ResizedImageField(
        verbose_name=_('Фото'),
        upload_to='defects/',
        blank=True,
        null=True,
        size=[1280, 720],
    )
    effects = models.ManyToManyField(
        to='defects.Effect',
        verbose_name=_('Последствия дефекта'),
        related_name='defects'
    )
    features = models.ManyToManyField(
        to='defects.Feature',
        verbose_name=_('Признаки дефекта'),
        related_name='defects'
    )
    condition = models.ForeignKey(
        to='defects.Condition',
        verbose_name=_('Условие обнаружения'),
        on_delete=models.PROTECT,
        related_name='defects'
    )
    repair = models.TextField(
        verbose_name=_('Выполненые мероприятия'),
        max_length=500,
        blank=True,
        null=True,
    )
    repair_date = models.DateField(
        verbose_name=_('Дата устранения'),
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('-date', )
        verbose_name = _('Дефект')
        verbose_name_plural = _('Дефекты')

    def clean(self):
        errors = {}
        if self.date > now().date():
            errors['date'] = ValidationError(
                _('Дата обнаружения дефекта не может быть в будущем')
            )
        if self.date > self.repair_date:
            errors['repair_date'] = ValidationError(
                _('Дата устранения дефекта не может быть раньше обнаружения')
            )
        if errors:
            raise ValidationError(errors)


class Effect(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=100,
        unique=True
    )
    slug = models.SlugField(
        verbose_name=_('Короткая ссылка'),
        unique=True
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Последствие дефекта')
        verbose_name_plural = _('Последствия дефекта')

    def __str__(self):
        return self.name


class Condition(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=100,
        unique=True
    )
    slug = models.SlugField(
        verbose_name=_('Короткая ссылка'),
        unique=True
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Условие обнаружения')
        verbose_name_plural = _('Условия обнаружения')

    def __str__(self):
        return self.name


class Feature(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=100,
        unique=True
    )
    slug = models.SlugField(
        verbose_name=_('Короткая ссылка'),
        unique=True
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Признак дефекта')
        verbose_name_plural = _('Признаки дефекта')

    def __str__(self):
        return self.name
