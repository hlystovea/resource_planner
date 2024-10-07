from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
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
        upload_to='protocols/e2/',
        validators=[FileExtensionValidator(('png', 'jpg', 'csv'))],
    )
    file_2 = models.FileField(
        verbose_name=_('Осциллограмма процесса возбуждения ВГ на АРВ2'),
        upload_to='protocols/e2/',
        validators=[FileExtensionValidator(('png', 'jpg', 'csv'))],
    )
    file_3 = models.FileField(
        verbose_name=_('Осциллограмма процесса гашения ТП ВГ на АРВ1'),
        upload_to='protocols/e2/',
        validators=[FileExtensionValidator(('png', 'jpg', 'csv'))],
    )
    file_4 = models.FileField(
        verbose_name=_('Осциллограмма процесса гашения ТП ВГ на АРВ2'),
        upload_to='protocols/e2/',
        validators=[FileExtensionValidator(('png', 'jpg', 'csv'))],
    )
    file_5 = models.FileField(
        verbose_name=_('Осциллограмма процесса возбуждения ГГ на АРВ1 в режиме (Ug)'),
        upload_to='protocols/e2/',
        validators=[FileExtensionValidator(('png', 'jpg', 'csv'))],
    )
    file_6 = models.FileField(
        verbose_name=_('Осциллограмма процесса возбуждения ГГ на АРВ2 в режиме (Ug)'),
        upload_to='protocols/e2/',
        validators=[FileExtensionValidator(('png', 'jpg', 'csv'))],
    )
    file_7 = models.FileField(
        verbose_name=_('Осциллограмма процесса возбуждения ГГ на АРВ1 в режиме (If)'),
        upload_to='protocols/e2/',
        validators=[FileExtensionValidator(('png', 'jpg', 'csv'))],
    )
    file_8 = models.FileField(
        verbose_name=_('Осциллограмма процесса возбуждения ГГ на АРВ2 в режиме (If)'),
        upload_to='protocols/e2/',
        validators=[FileExtensionValidator(('png', 'jpg', 'csv'))],
    )
    file_9 = models.FileField(
        verbose_name=_('Осциллограмма процесса гашения ГГ на АРВ1'),
        upload_to='protocols/e2/',
        validators=[FileExtensionValidator(('png', 'jpg', 'csv'))],
    )
    file_10 = models.FileField(
        verbose_name=_('Осциллограмма процесса гашения ГГ на АРВ2'),
        upload_to='protocols/e2/',
        validators=[FileExtensionValidator(('png', 'jpg', 'csv'))],
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


class Protocol(models.Model):
    date = models.DateField(
        verbose_name=_('Дата проверки')
    )
    template = models.ForeignKey(
        to='docs.Template',
        verbose_name=_('Шаблон'),
        on_delete=models.PROTECT
    )
    connection = models.ForeignKey(
        to='hardware.Connection',
        verbose_name=_('Присоединение'),
        on_delete=models.CASCADE,
        related_name='protocols'
    )
    signers = models.ManyToManyField(
        to='staff.Employee',
        verbose_name=_('Подписывающие'),
        related_name='protocols'
    )
    supervisor = models.ForeignKey(
        to='staff.Employee',
        verbose_name=_('Проверяющий'),
        on_delete=models.PROTECT
    )
    instruments = models.ManyToManyField(
        to='warehouse.Instrument',
        verbose_name=_('Инструменты'),
        related_name='protocols',
        blank=True
    )

    class Meta:
        ordering = ('date', )
        verbose_name = _('Протокол ТО')
        verbose_name_plural = _('Протоколы ТО')

    def clean(self):
        errors = {}
        if self.date and self.date > now().date():
            errors['date'] = ValidationError(
                _('Дата проверки не может быть в будущем')
            )
        if errors:
            raise ValidationError(errors)

    def get_absolute_url(self):
        return reverse('docs:protocol-detail', kwargs={'pk': self.pk})


class Template(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
        unique=True
    )
    file = models.FileField(
        verbose_name=_('HTML-шаблон'),
        upload_to='docs/protocols/templates/',
        validators=[FileExtensionValidator(('html', ))]
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Шаблон протокола')
        verbose_name_plural = _('Шаблоны протоколов')

    def get_absolute_url(self):
        return reverse('docs:template-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class BaseElement(models.Model):
    slug = models.SlugField(
        verbose_name=_('Наименование элемента'),
        max_length=50
    )
    protocol = models.ForeignKey(
        to='docs.Protocol',
        verbose_name=_('Протокол'),
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class File(BaseElement):
    value = models.FileField(
        verbose_name=_('Файл'),
        upload_to='docs/protocols/files',
        validators=[FileExtensionValidator(('png', 'jpg', 'csv'))]
    )

    class Meta:
        verbose_name = _('Файл')
        verbose_name_plural = _('Файлы')
        constraints = [
            models.UniqueConstraint(
                fields=('slug', 'protocol'),
                name='file_slug_protocol_uniquetogether',
            ),
        ]


class Text(BaseElement):
    value = models.TextField(verbose_name=_('Текст'))

    class Meta:
        verbose_name = _('Текст')
        verbose_name_plural = _('Тексты')
        constraints = [
            models.UniqueConstraint(
                fields=('slug', 'protocol'),
                name='text_slug_protocol_uniquetogether',
            ),
        ]
