from django.contrib.auth.models import AbstractUser
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
        max_length=30,
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


class Employee(AbstractUser):
    patronymic = models.CharField(
        verbose_name=_('Отчество'),
        max_length=150,
        blank=True
    )
    dept = models.ForeignKey(
        Dept,
        verbose_name=_('Подразделение'),
        on_delete=models.CASCADE,
        related_name='employees',
        null=True
    )
    is_chief = models.BooleanField(
        verbose_name=_('Руководитель подразделения'),
        default=False
    )

    def __str__(self):
        if self.last_name:
            return f'{self.last_name} {self.first_name[:1]}.{self.patronymic[:1]}.'  # noqa(E501)
        return self.username
