import pytest
from django.db.models import fields
from django.urls import reverse
from django_resized import ResizedImageField

from staff.models import Dept
from tests.common import get_field_context, search_field
from warehouse.forms import InstrumentForm
from warehouse.models import Instrument


class TestInstrument:
    test_args = [
        ('some-name', 'number', 'number'),
        ('foo', 'bar', '123'),
        ('12', '11', '10'),
    ]

    def test_instrument_model(self):
        model_fields = Instrument._meta.fields

        name_field = search_field(model_fields, 'name')
        assert name_field is not None, \
            'Модель Instrument должна содержать поле name'
        assert type(name_field) == fields.CharField, \
            'Поле name модели Instrument должно быть текстовым CharField'
        assert not name_field.blank, \
            'Поле name модели Instrument должно быть обязательным'

        inventory_number_field = search_field(model_fields, 'inventory_number')
        assert inventory_number_field is not None, \
            'Модель Instrument должна содержать поле inventory_number'
        assert type(inventory_number_field) == fields.CharField, \
            'Поле inventory_number должно быть текстовым CharField'
        assert inventory_number_field.blank, \
            'Поле inventory_number не должно быть обязательным'

        serial_number_field = search_field(model_fields, 'serial_number')
        assert serial_number_field is not None, \
            'Модель Instrument должна содержать поле serial_number'
        assert type(serial_number_field) == fields.CharField, \
            'Поле serial_number должно быть текстовым CharField'
        assert serial_number_field.blank, \
            'Поле serial_number модели Instrument не должно быть обязательным'

        owner_field = search_field(model_fields, 'owner_id')
        assert owner_field is not None, \
            'Модель Instrument должна содержать поле owner'
        assert type(owner_field) == fields.related.ForeignKey, \
            'Поле owner модели Instrument должно быть ссылкой на другую модель'
        assert owner_field.related_model == Dept, \
            'Поле owner модели Instrument должно быть ссылкой на модель Dept'
        assert not owner_field.blank, \
            'Поле owner_field модели Instrument должно быть обязательным'

        image_field = search_field(model_fields, 'image')
        assert image_field is not None, \
            'Модель Instrument должна содержать поле image'
        assert type(image_field) == ResizedImageField, \
            'Поле image модели Instrument должно быть ResizedImageField'
        assert image_field.blank, \
            'Поле image модели Instrument не должно быть обязательным'

    @pytest.mark.django_db
    def test_instrument_view_get_list(self, client):
        try:
            url = reverse('warehouse:instrument-list')
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert response.templates[0].name == 'warehouse/instrument_list.html', \
            'Проверьте, что используете шаблон instrument_list.html в ответе'
        assert 'instrument_list' in response.context, \
            'Проверьте, что передали поле "instrument_list" в контекст стр.'
        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'

        response = client.get(url, headers={'Hx-Request': True})
        assert response.templates[0].name == 'warehouse/instrument_table.html', \
            'Проверьте, что используете шаблон instrument_table.html в ответе ' \
            'для htmx запроса'

    @pytest.mark.django_db
    def test_instrument_view_get_detail(self, client, instrument):
        try:
            url = reverse(
                'warehouse:instrument-detail', kwargs={'pk': instrument.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        instrument = get_field_context(response.context, Instrument)
        assert instrument, \
            'Проверьте, что передали поле типа Instrument в контекст страницы'

        response = client.get(url, headers={'Hx-Request': True})
        assert response.templates[0].name == 'warehouse/instrument_row.html', \
            'Проверьте, что используете шаблон instrument_row.html в ответе ' \
            'для htmx запроса'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name, inventory_number, serial_number', test_args)
    def test_instrument_view_create(
        self, name, inventory_number, serial_number, auto_login_user
    ):
        client, user = auto_login_user()
        url = reverse('warehouse:instrument-create')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], InstrumentForm), \
            'Проверьте, что поле `form` содержит объект класса `MaterialForm`'
        assert 'is_new' in response.context, \
            'Проверьте, что передали поле `is_new` в контекст страницы'
        assert response.context['is_new'], \
            'Проверьте, что значение поля `is_new` в контексте стр. = `True`'

        data = {
            'name': name,
            'inventory_number': inventory_number,
            'serial_number': serial_number,
        }
        try:
            response = client.post(url, follow=True, data=data)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        instrument = get_field_context(response.context, Instrument)

        assert response.templates[0].name == 'warehouse/instrument_detail.html', \
            'Проверьте, что используете шаблон material_instrument.html в ответе'
        assert instrument is not None, \
            'Проверьте, что передали поле типа Instrument в контекст страницы'
        assert data['name'] == instrument.name, \
            'Проверьте, что сохраненный экземпляр `instrument` содержит ' \
            'соответствующее поле `name`'
        assert data['inventory_number'] == instrument.inventory_number, \
            'Проверьте, что измененный экземпляр `instrument` содержит ' \
            'соответствующее поле `inventory_number`'
        assert data['serial_number'] == instrument.serial_number, \
            'Проверьте, что измененный экземпляр `instrument` содержит ' \
            'соответствующее поле `serial_number`'

        headers = {'Hx-Request': True}
        response = client.post(url, follow=True, data=data, headers=headers)
        assert response.templates[0].name == 'warehouse/instrument_row.html', \
            'Проверьте, что используете шаблон instrument_row.html в ответе ' \
            'для htmx запроса'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name, inventory_number, serial_number', test_args)
    def test_inventory_number_view_update(
        self, name, inventory_number, serial_number, auto_login_user, instrument
    ):
        client, user = auto_login_user()
        url = reverse('warehouse:instrument-update', kwargs={'pk': instrument.pk})

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], InstrumentForm), \
            'Проверьте, что поле `form` содержит объект класса `MaterialForm`'

        response = client.get(url, headers={'Hx-Request': True})
        assert response.templates[0].name == 'warehouse/instrument_inline_form.html', \
            'Проверьте, что используете шаблон instrument_inline_form.html в ответе ' \
            'для htmx запроса'

        data = {
            'name': name,
            'inventory_number': inventory_number,
            'serial_number': serial_number,
        }
        try:
            response = client.post(url, follow=True, data=data)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        instrument = get_field_context(response.context, Instrument)

        assert instrument is not None, \
            'Проверьте, что передали поле типа Material в контекст страницы'
        assert data['name'] == instrument.name, \
            'Проверьте, что сохраненный экземпляр `instrument` содержит' \
            'соответствующее поле `name`'
        assert data['inventory_number'] == instrument.inventory_number, \
            'Проверьте, что измененный экземпляр `instrument` содержит' \
            'соответствующее поле `inventory_number`'
        assert data['serial_number'] == instrument.serial_number, \
            'Проверьте, что измененный экземпляр `instrument` содержит' \
            'соответствующее поле `serial_number`'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name, inventory_number, serial_number', test_args)
    def test_material_view_delete(
        self, name, inventory_number, serial_number, auto_login_user
    ):
        client, user = auto_login_user()
        instrument = Instrument.objects.create(
            name=name,
            inventory_number=inventory_number,
            serial_number=serial_number
        )
        queryset = Instrument.objects.filter(
            name=name,
            inventory_number=inventory_number,
            serial_number=serial_number
        )

        assert queryset.exists(), \
            'Тест работает неправильно, экземпляр `material` отсутствует в БД'

        url = reverse('warehouse:instrument-delete', kwargs={'pk': instrument.pk})

        try:
            response = client.delete(url, follow=True)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert not queryset.exists(), \
            'Проверьте, что эксземпляр `material` удаляется из БД'
        
        instrument = Instrument.objects.create(
            name=name,
            inventory_number=inventory_number,
            serial_number=serial_number
        )
        url = reverse('warehouse:instrument-delete', kwargs={'pk': instrument.pk})
        response = client.delete(url, headers={'Hx-Request': True})

        assert response.status_code == 200
        assert len(response.content) == 0, \
            'Проверьте, что на htmx запрос возвращется пустой ответ'

    @pytest.mark.django_db
    def test_instrument_filters(
        self, client, instrument_dept1, instrument_dept2
    ):
        url = reverse('warehouse:instrument-list')
        instruments = Instrument.objects.all()

        response = client.get(url)
        instrument_list = response.context['instrument_list']

        assert len(instrument_list) == len(instruments), \
            'Проверьте, что без фильтрации передаются все объекты'

        response = client.get(f'{url}?dept={instrument_dept1.owner.pk}')
        instrument_list = response.context['instrument_list']

        assert instrument_dept1 in instrument_list, \
            'Фильтр по подразделению работает не правильно'
        assert instrument_dept2 not in instrument_list, \
            'Фильтр по подразделению работает не правильно'
