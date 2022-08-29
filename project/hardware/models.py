from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Facility(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
        unique=True
    )
    abbreviation = models.CharField(
        verbose_name=_('Аббревиатура'),
        max_length=30,
        unique=True
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Объект диспетчеризации')
        verbose_name_plural = _('Объекты диспетчеризации')

    def __str__(self):
        return self.abbreviation


class Connection(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200
    )
    abbreviation = models.CharField(
        verbose_name=_('Аббревиатура'),
        max_length=30
    )
    facility = models.ForeignKey(
        to='hardware.Facility',
        verbose_name=_('Объект диспетчеризации'),
        on_delete=models.CASCADE,
        related_name='connections'
    )

    class Meta:
        ordering = ('facility', 'abbreviation')
        verbose_name = _('Присоединение')
        verbose_name_plural = _('Присоединения')
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'facility'),
                name='name_facility_uniquetogether'
            ),
            models.UniqueConstraint(
                fields=('abbreviation', 'facility'),
                name='abbreviation_facility_uniquetogether'
            )
        ]

    def __str__(self):
        return f'{self.facility}/{self.abbreviation}'


class Group(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
        unique=True
    )
    abbreviation = models.CharField(
        verbose_name=_('Аббревиатура'),
        max_length=30,
        unique=True
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Группа оборудования')
        verbose_name_plural = _('Группы оборудования')

    def __str__(self):
        return self.abbreviation


class Hardware(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
    )
    inventory_number = models.CharField(
        verbose_name=_('Инв. номер'),
        max_length=50,
        unique=True
    )
    connection = models.ForeignKey(
        to='hardware.Connection',
        verbose_name=_('Присоединение'),
        on_delete=models.SET_NULL,
        related_name='hardware',
        null=True
    )
    group = models.ForeignKey(
        to='hardware.Group',
        verbose_name=_('Группа оборудования'),
        on_delete=models.SET_NULL,
        related_name='hardware',
        null=True
    )

    class Meta:
        ordering = ('connection', 'name')
        verbose_name = _('Оборудование')
        verbose_name_plural = _('Оборудование')
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'connection'),
                name='name_connection_uniquetogether'
            )
        ]

    def __str__(self):
        if self.connection:
            return f'{self.connection}/{self.name} (Инв.№{self.inventory_number})'  # noqa(E501)
        return f'{self.name} (Инв.№{self.inventory_number})'


class Cabinet(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
    )
    abbreviation = models.CharField(
        verbose_name=_('Оперативное наименование'),
        max_length=30,
    )
    hardware = models.ForeignKey(
        to='hardware.Hardware',
        verbose_name=_('Оборудование'),
        on_delete=models.CASCADE,
        related_name='cabinets'
    )
    manufacturer = models.CharField(
        verbose_name=_('Изготовитель'),
        max_length=200,
    )
    series = models.CharField(
        verbose_name=_('Серия изделия'),
        max_length=100,
        blank=True,
        null=True
    )
    type = models.CharField(
        verbose_name=_('Тип изделия'),
        max_length=100,
        blank=True,
        null=True
    )
    release_year = models.IntegerField(
        verbose_name=_('Год выпуска'),
        validators=[
            MinValueValidator(1972),
            MaxValueValidator(2050)
        ]
    )
    launch_year = models.IntegerField(
        verbose_name=_('Год ввода в эксплуатацию'),
        validators=[
            MinValueValidator(1972),
            MaxValueValidator(2050)
        ]
    )

    class Meta:
        ordering = ('hardware', 'abbreviation')
        verbose_name = _('Шкаф/панель')
        verbose_name_plural = _('Шкафы/панели')
        constraints = [
            models.UniqueConstraint(
                fields=('abbreviation', 'hardware'),
                name='abbreviation_hardware_uniquetogether'
            )
        ]

    def clean(self):
        errors = {}
        if self.release_year and self.launch_year:
            if self.release_year > self.launch_year:
                errors['release_year'] = ValidationError(
                    _('Год выпуска не может быть позже ввода в эксплуатацию')
                )
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f'{self.abbreviation}'


class Component(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
    )
    function = models.ForeignKey(
        to='hardware.ComponentFunction',
        verbose_name=_('Назначение'),
        on_delete=models.PROTECT,
        related_name='components'
    )
    design = models.ForeignKey(
        to='hardware.ComponentDesign',
        verbose_name=_('Исполнение'),
        on_delete=models.PROTECT,
        related_name='components'
    )
    manufacturer = models.CharField(
        verbose_name=_('Изготовитель'),
        max_length=200,
    )
    series = models.CharField(
        verbose_name=_('Серия изделия'),
        max_length=100,
        blank=True,
        null=True
    )
    type = models.CharField(
        verbose_name=_('Тип изделия'),
        max_length=100,
        blank=True,
        null=True
    )
    release_year = models.IntegerField(
        verbose_name=_('Год выпуска'),
        validators=[
            MinValueValidator(1972),
            MaxValueValidator(2050)
        ]
    )
    launch_year = models.IntegerField(
        verbose_name=_('Год ввода в эксплуатацию'),
        validators=[
            MinValueValidator(1972),
            MaxValueValidator(2050)
        ]
    )
    repair_method = models.ForeignKey(
        to='hardware.ComponentRepairMethod',
        verbose_name=_('Метод устранения дефекта'),
        on_delete=models.PROTECT,
        related_name='components'
    )
    cabinet = models.ForeignKey(
        to='hardware.Cabinet',
        verbose_name=_('Шкаф/Панель'),
        on_delete=models.CASCADE,
        related_name='components'
    )
    component = models.ForeignKey(
        to='hardware.Component',
        verbose_name=_('Комплектующее'),
        on_delete=models.SET_NULL,
        related_name='components',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Комплектующее изделие')
        verbose_name_plural = _('Комплектующие изделия')

    def clean(self):
        errors = {}
        if self.component and self.cabinet:
            if self.component.cabinet != self.cabinet:
                errors['component'] = ValidationError(
                    _('Комплектующее не может быть из другого шкафа/панели')
                )
        if self.release_year and self.launch_year:
            if self.release_year > self.launch_year:
                errors['release_year'] = ValidationError(
                    _('Год выпуска не может быть позже ввода в эксплуатацию')
                )
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f'{self.name}'


class ComponentRepairMethod(models.Model):
    name = models.CharField(
        verbose_name=_('Метод устранения дефекта'),
        max_length=200,
        unique=True
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Метод устранения дефекта')
        verbose_name_plural = _('Методы устранения дефектов')
    
    def __str__(self):
        return self.name


class ComponentDesign(models.Model):
    name = models.CharField(
        verbose_name=_('Исполнение'),
        max_length=200,
        unique=True
    )
    abbreviation = models.CharField(
        verbose_name=_('Аббревиатура'),
        max_length=3,
        unique=True
    )

    class Meta:
        ordering = ('id', )
        verbose_name = _('Вариант исполнения')
        verbose_name_plural = _('Варианты исполнения')
    
    def __str__(self):
        return f'{self.abbreviation} - {self.name}'


class ComponentFunction(models.Model):
    name = models.CharField(
        verbose_name=_('Назначение комплектующего'),
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Назначение комплектующего')
        verbose_name_plural = _('Назначения комплектующих')
    
    def __str__(self):
        return self.name
