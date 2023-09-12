from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField


class Defect(models.Model):
    date = models.DateField(
        verbose_name=_('Дата обнаружения'),
    )
    part = models.ForeignKey(
        to='hardware.Part',
        verbose_name=_('Комплектующее'),
        on_delete=models.CASCADE,
        related_name='defects',
        null=True,
    )
    employee = models.ForeignKey(
        to='staff.Employee',
        verbose_name=_('Сотрудник обнаруживший дефект'),
        on_delete=models.PROTECT,
        related_name='defects',
    )
    description = models.TextField(
        verbose_name=_('Описание дефекта'),
    )
    image = ResizedImageField(
        verbose_name=_('Фото'),
        upload_to='defects/images/%Y/%m/%d/',
        blank=True,
        null=True,
        size=[1280, 720],
    )
    effects = models.ManyToManyField(
        to='defects.Effect',
        verbose_name=_('Последствия дефекта'),
        related_name='defects',
    )
    features = models.ManyToManyField(
        to='defects.Feature',
        verbose_name=_('Признаки дефекта'),
        related_name='defects',
    )
    condition = models.ForeignKey(
        to='defects.Condition',
        verbose_name=_('Условие обнаружения'),
        on_delete=models.PROTECT,
        related_name='defects',
    )
    technical_reasons = models.ManyToManyField(
        to='defects.TechnicalReason',
        verbose_name=_('Технические причины дефекта'),
        related_name='defects',
        blank=True,
    )
    organizational_reasons = models.ManyToManyField(
        to='defects.OrganizationalReason',
        verbose_name=_('Организационные причины'),
        related_name='defects',
        blank=True,
    )
    repair = models.TextField(
        verbose_name=_('Выполненные мероприятия'),
        blank=True,
        null=True,
    )
    repair_date = models.DateField(
        verbose_name=_('Дата устранения'),
        blank=True,
        null=True,
    )
    repair_method = models.ForeignKey(
        to='defects.RepairMethod',
        verbose_name=_('Метод устранения'),
        on_delete=models.PROTECT,
        related_name='defects',
        blank=True,
        null=True,
    )
    attachment = models.FileField(
        verbose_name=_('Приложение'),
        upload_to='defects/attachments/%Y/%m/%d/',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('-date', )
        verbose_name = _('Дефект')
        verbose_name_plural = _('Дефекты')

    def clean(self):
        errors = {}
        if self.date and self.date > now().date():
            errors['date'] = ValidationError(
                _('Дата обнаружения дефекта не может быть в будущем')
            )
        if self.repair_date and self.date:
            if self.date > self.repair_date:
                errors['repair_date'] = ValidationError(
                    _('Дата устранения дефекта не может быть раньше обнаружения')
                )
        if errors:
            raise ValidationError(errors)

    def get_absolute_url(self):
        return reverse('defects:defect-detail', kwargs={'pk': self.pk})


class Effect(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=100,
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

    class Meta:
        ordering = ('name', )
        verbose_name = _('Признак дефекта')
        verbose_name_plural = _('Признаки дефекта')

    def __str__(self):
        return self.name


class TechnicalReason(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
        unique=True
    )
    is_dependent = models.BooleanField(
        verbose_name=_('Зависит от внешних условий'),
        default=False
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Техническая причина')
        verbose_name_plural = _('Технические причины')

    def __str__(self):
        return self.name


class OrganizationalReason(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
        unique=True
    )
    is_dependent = models.BooleanField(
        verbose_name=_('Зависит от внешних условий'),
        default=False
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Организационная причина')
        verbose_name_plural = _('Организационные причины')

    def __str__(self):
        return self.name


class RepairMethod(models.Model):
    name = models.CharField(
        verbose_name=_('Метод устранения'),
        max_length=200,
        unique=True,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Метод устранения')
        verbose_name_plural = _('Методы устранения')

    def __str__(self):
        return self.name
