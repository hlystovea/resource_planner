import pytest

from django.db.models import fields
from django.urls import reverse
from django_resized import ResizedImageField

from warehouse.forms import DeptForm
from warehouse.models import Instrument
from staff.models import Dept
from common import search_field


class TestInstrument:
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
        assert 'instrument_list' in response.context, \
            'Проверьте, что передали поле "instrument_list" в контекст стр.'
        assert type(response.context.get('form')) == DeptForm, \
            'Проверьте, что передали поле типа DeptForm в контекст стр.'

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
        assert type(response.context.get('instrument')) == Instrument, \
            'Проверьте, что передали поле типа Instrument в контекст страницы'
