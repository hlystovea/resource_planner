import pytest

from django.db.models import fields
from django.urls import reverse
from django_resized import ResizedImageField
from qr_code.qrcode.utils import QRCodeOptions

from warehouse.forms import DeptForm
from warehouse.models import Instrument, Material, MaterialStorage, Storage
from staff.models import Dept


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


def get_field_context(context, field_type):
    for field in context.keys():
        if field not in ('user', 'request') and type(context[field]) == field_type:
            return context[field]


class TestInstrument:

    def test_instrument_model(self):
        model_fields = Instrument._meta.fields

        name_field = search_field(model_fields, 'name')
        assert name_field is not None, 'Модель Instrument должна содержать поле name'
        assert type(name_field) == fields.CharField, \
            'Поле name модели Instrument должно быть текстовым CharField'
        assert not name_field.blank, \
            'Поле name модели Instrument должно быть обязательным'

        inventory_number_field = search_field(model_fields, 'inventory_number')
        assert inventory_number_field is not None, \
            'Модель Instrument должна содержать поле inventory_number'
        assert type(inventory_number_field) == fields.CharField, \
            'Поле inventory_number модели Instrument должно быть текстовым CharField'
        assert inventory_number_field.blank, \
            'Поле inventory_number модели Instrument не должно быть обязательным'

        serial_number_field = search_field(model_fields, 'serial_number')
        assert serial_number_field is not None, \
            'Модель Instrument должна содержать поле serial_number'
        assert type(serial_number_field) == fields.CharField, \
            'Поле serial_number модели Instrument должно быть текстовым CharField'
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
            'Проверьте, что передали поле "instrument_list" в контекст страницы'
        assert type(response.context.get('form')) == DeptForm, \
            'Проверьте, что передали поле типа DeptForm в контекст страницы'

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


class TestStorage:

    def test_storage_model(self):
        model_fields = Storage._meta.fields

        name_field = search_field(model_fields, 'name')
        assert name_field is not None, 'Модель Storage должна содержать поле name'
        assert type(name_field) == fields.CharField, \
            'Поле name модели Storage должно быть текстовым CharField'
        assert not name_field.blank, \
            'Поле name модели Storage должно быть обязательным'

        parent_storage_field = search_field(model_fields, 'parent_storage_id')
        assert parent_storage_field is not None, \
            'Модель Storage должна содержать поле parent_storage'
        assert type(parent_storage_field) == fields.related.ForeignKey, \
            'Поле parent_storage модели Storage должно быть ссылкой на другую модель'
        assert parent_storage_field.related_model == Storage, \
            'Поле parent_storage модели Storage должно быть ссылкой на модель Storage'
        assert parent_storage_field.blank, \
            'Поле parent_storage модели Storage не должно быть обязательным'

    @pytest.mark.django_db
    def test_storage_view_get_qrcode(self, client, storage_1):
        try:
            url = reverse(
                'warehouse:storage-qrcode', kwargs={'pk': storage_1.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200
        assert type(response.context.get('storage')) == Storage, \
            'Проверьте, что передали поле типа Storage в контекст страницы'
        assert type(response.context.get('qr_options')) == QRCodeOptions, \
            'Проверьте, что передали поле типа QRCodeOptions в контекст страницы'
        assert 'storage_url' in response.context, \
            'Проверьте, что передали поле "storage_url" в контекст страницы'
        assert 'internal_storage_urls' in response.context, \
            'Проверьте, что передали поле "internal_storage_urls" в контекст страницы'

    @pytest.mark.django_db
    def test_storage_view_get_list(self, client):
        try:
            url = reverse('warehouse:storage-list')
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200
        assert 'storage_list' in response.context, \
            'Проверьте, что передали поле "storage_list" в контекст страницы'

    @pytest.mark.django_db
    def test_storage_view_get_detail(self, client, storage_1):
        try:
            url = reverse(
                'warehouse:storage-detail', kwargs={'pk': storage_1.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200
        storage_from_context = get_field_context(response.context, Storage)
        assert storage_from_context is not None, \
            'Проверьте, что передали поле типа Storage в контекст страницы'

    @pytest.mark.django_db
    def test_storage_view_create(self, auto_login_user, employee_1):
        client, user = auto_login_user()

        try:
            url = reverse('warehouse:storage-create')
            response = client.get(url, follow=True)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'is_new' in response.context, \
            'Проверьте, что передали поле `is_new` в контекст страницы'

        try:
            url = reverse('warehouse:storage-create')
            data = {
                'name': 'some-storage-name',
            }
            response = client.post(url, follow=True, data=data)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200


class TestMaterial:

    def test_material_model(self):
        model_fields = Material._meta.fields

        name_field = search_field(model_fields, 'name')
        assert name_field is not None, 'Модель Material должна содержать поле name'
        assert type(name_field) == fields.CharField, \
            'Поле name модели Material должно быть текстовым CharField'
        assert not name_field.blank, \
            'Поле name модели Material должно быть обязательным'

        measurement_unit_field = search_field(model_fields, 'measurement_unit')
        assert measurement_unit_field is not None, \
            'Модель Material должна содержать поле measurement_unit'
        assert type(measurement_unit_field) == fields.CharField, \
            'Поле measurement_unit модели Material должно быть текстовым CharField'
        assert not measurement_unit_field.blank, \
            'Поле measurement_unit модели Material должно быть обязательным'

        article_number_field = search_field(model_fields, 'article_number')
        assert article_number_field is not None, \
            'Модель Material должна содержать поле article_number'
        assert type(article_number_field) == fields.CharField, \
            'Поле article_number модели Material должно быть текстовым CharField'
        assert article_number_field.blank, \
            'Поле article_number модели Material не должно быть обязательным'

        image_field = search_field(model_fields, 'image')
        assert image_field is not None, \
            'Модель Material должна содержать поле image'
        assert type(image_field) == ResizedImageField, \
            'Поле image модели Material должно быть ResizedImageField'
        assert image_field.blank, \
            'Поле image модели Material не должно быть обязательным'

    def test_material_storage_model(self):
        model_fields = MaterialStorage._meta.fields

        material_field = search_field(model_fields, 'material_id')
        assert material_field is not None, \
            'Модель MaterialStorage должна содержать поле material'
        assert type(material_field) == fields.related.ForeignKey, \
            'Поле material модели MaterialStorage должно быть ссылкой на другую модель'
        assert material_field.related_model == Material, \
            'Поле material модели MaterialStorage должно быть ссылкой на модель Material'
        assert not material_field.blank, \
            'Поле material модели MaterialStorage должно быть обязательным'

        inventory_number_field = search_field(model_fields, 'inventory_number')
        assert inventory_number_field is not None, \
            'Модель MaterialStorage должна содержать поле inventory_number'
        assert type(inventory_number_field) == fields.CharField, \
            'Поле inventory_number модели MaterialStorage должно быть текстовым CharField'
        assert inventory_number_field.blank, \
            'Поле inventory_number модели MaterialStorage не должно быть обязательным'

        amount_field = search_field(model_fields, 'amount')
        assert amount_field is not None, \
            'Модель MaterialStorage должна содержать поле amount'
        assert type(amount_field) == fields.FloatField, \
            'Поле amount модели MaterialStorage должно быть числовым FloatField'
        assert not amount_field.blank, \
            'Поле amount модели MaterialStorage должно быть обязательным'

        owner_field = search_field(model_fields, 'owner_id')
        assert owner_field is not None, \
            'Модель MaterialStorage должна содержать поле owner'
        assert type(owner_field) == fields.related.ForeignKey, \
            'Поле owner модели MaterialStorage должно быть ссылкой на другую модель'
        assert owner_field.related_model == Dept, \
            'Поле owner модели MaterialStorage должно быть ссылкой на модель Dept'
        assert owner_field.blank, \
            'Поле owner модели MaterialStorage не должно быть обязательным'

        storage_field = search_field(model_fields, 'storage_id')
        assert storage_field is not None, \
            'Модель MaterialStorage должна содержать поле storage'
        assert type(storage_field) == fields.related.ForeignKey, \
            'Поле storage модели MaterialStorage должно быть ссылкой на другую модель'
        assert storage_field.related_model == Storage, \
            'Поле storage модели MaterialStorage должно быть ссылкой на модель Storage'
        assert not storage_field.blank, \
            'Поле storage модели MaterialStorage должно быть обязательным'

    @pytest.mark.django_db
    def test_material_view_get_list(self, client):
        try:
            url = reverse('warehouse:material-list')
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200
        assert 'material_list' in response.context, \
            'Проверьте, что передали поле "material_list" в контекст страницы'
        assert type(response.context.get('form')) == DeptForm, \
            'Проверьте, что передали поле типа DeptForm в контекст страницы'

    @pytest.mark.django_db
    def test_material_view_get_detail(self, client, material, material_in_storage_1, material_in_storage_2):
        try:
            url = reverse(
                'warehouse:material-detail', kwargs={'pk': material.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200, \
            'Статус код страницы должен быть 200'

        material_from_context = get_field_context(response.context, Material)

        assert material_from_context is not None, \
            'Проверьте, что передали поле типа Material в контекст страницы'
        assert type(material_from_context.amount.first()) == MaterialStorage, \
            'Проверьте, что вместе с объектом Material передали поле типа MaterialStorage в контекст страницы'
        assert material_from_context.total == material_in_storage_1.amount + material_in_storage_2.amount, \
            'Проверьте, что объект Material содержит поле total с общим количеством материала'
