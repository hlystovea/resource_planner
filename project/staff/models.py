from django.db import models
from django.utils.translation import gettext_lazy as _


class Service(models.Model):
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=100,
    )
    abbreviation = models.CharField(
        verbose_name=_('Аббревиатура'),
        max_length=10,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Служба')
        verbose_name_plural = _('Службы')

    def __str__(self):
        return self.abbreviation


class Dept(models.Model):
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=100,
    )
    abbreviation = models.CharField(
        verbose_name=_('Аббревиатура'),
        max_length=10,
    )
    service = models.ForeignKey(
        to=Service,
        verbose_name=_('Служба'),
        on_delete=models.CASCADE,
        related_name='departments',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Участок/группа/отдел')
        verbose_name_plural = _('Участки/группы/отделы')

    def __str__(self):
        return self.abbreviation


class Staff(models.Model):
    last_name = models.CharField(
        verbose_name=_('Фамилия'),
        max_length=20,
    )
    first_name = models.CharField(
        verbose_name=_('Имя'),
        max_length=20,
    )
    patronymic = models.CharField(
        verbose_name=_('Отчество'),
        max_length=20,
    )
    department = models.ForeignKey(
        to=Dept,
        verbose_name=_('Подразделение'),
        on_delete=models.CASCADE,
        related_name='staff',
    )

    class Meta:
        ordering = ('last_name', )
        verbose_name = _('Сотрудник')
        verbose_name_plural = _('Сотрудники')

    def __str__(self):
        return self.last_name + self.first_name + self.patronymic
