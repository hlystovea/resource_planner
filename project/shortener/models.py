from django.db import models
from django.utils.translation import gettext_lazy as _


class Shortener(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_('Время создания'),
        auto_now_add=True
    )
    long_url = models.URLField(
        verbose_name=_('Исходный адрес'),
    )
    short_url = models.CharField(
        verbose_name=_('Короткий адрес'),
        max_length=15,
        unique=True,
        blank=True,
    )

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('Сокращенная ссылка')
        verbose_name_plural = _('Сокращенные ссылки')

    def __str__(self):
        return f'{self.short_url} to {self.long_url}'
