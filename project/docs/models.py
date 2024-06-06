from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class ProtocolE2(models.Model):
    date = models.DateField(
        verbose_name=_('Дата проверки')
    )
    connection = models.ForeignKey(
        to='hardware.Connection',
        verbose_name=_('Присоединение'),
        on_delete=models.CASCADE,
        related_name='protocol_e2'
    )
    signers = models.ManyToManyField(
        to='staff.Employee',
        verbose_name=_('Подписывающие'),
        related_name='protocol_e2',
    )
    supervisor = models.ForeignKey(
        to='staff.Employee',
        verbose_name=_('Проверяющий'),
        on_delete=models.PROTECT,
    )
    instruments = models.ManyToManyField(
        to='warehouse.Instrument',
        verbose_name=_('Инструменты'),
        related_name='protocol_e2',
    )
    file_1 = models.FileField(
        verbose_name=_('Осциллограмма процесса возбуждения ВГ на АРВ1'),
        upload_to='protocols/e2/'
    )
    file_2 = models.FileField(
        verbose_name=_('Осциллограмма процесса возбуждения ВГ на АРВ2'),
        upload_to='protocols/e2/'
    )
    file_3 = models.FileField(
        verbose_name=_('Осциллограмма процесса гашения ТП ВГ на АРВ1'),
        upload_to='protocols/e2/'
    )
    file_4 = models.FileField(
        verbose_name=_('Осциллограмма процесса гашения ТП ВГ на АРВ2'),
        upload_to='protocols/e2/'
    )
    file_5 = models.FileField(
        verbose_name=_('Осциллограмма процесса возбуждения ГГ на АРВ1 в режиме (Ug)'),
        upload_to='protocols/e2/'
    )
    file_6 = models.FileField(
        verbose_name=_('Осциллограмма процесса возбуждения ГГ на АРВ2 в режиме (Ug)'),
        upload_to='protocols/e2/'
    )
    file_7 = models.FileField(
        verbose_name=_('Осциллограмма процесса возбуждения ГГ на АРВ1 в режиме (If)'),
        upload_to='protocols/e2/'
    )
    file_8 = models.FileField(
        verbose_name=_('Осциллограмма процесса возбуждения ГГ на АРВ2 в режиме (If)'),
        upload_to='protocols/e2/'
    )
    file_9 = models.FileField(
        verbose_name=_('Осциллограмма процесса гашения ГГ на АРВ1'),
        upload_to='protocols/e2/'
    )
    file_10 = models.FileField(
        verbose_name=_('Осциллограмма процесса гашения ГГ на АРВ2'),
        upload_to='protocols/e2/'
    )

    class Meta:
        ordering = ('date', )
        verbose_name = _('Протокол Э2')
        verbose_name_plural = _('Протоколы Э2')
        constraints = [
            models.UniqueConstraint(
                fields=('date', 'connection'),
                name='date_connection_uniquetogether',
            ),
        ]

    def clean(self):
        errors = {}
        if self.date and self.date > now().date():
            errors['date'] = ValidationError(
                _('Дата проверки не может быть в будущем')
            )
        if errors:
            raise ValidationError(errors)

    def get_absolute_url(self):
        return reverse('docs:protocol_e2-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'Протокол Э2 {self.connection} от {self.date}'
