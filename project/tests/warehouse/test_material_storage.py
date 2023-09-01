from django.db.models import fields

from common import search_field
from staff.models import Dept
from warehouse.models import Material, MaterialStorage, Storage


class TestMaterialStorage:
    def test_material_storage_model(self):
        model_fields = MaterialStorage._meta.fields

        material_field = search_field(model_fields, 'material_id')
        assert material_field is not None, \
            'Модель MaterialStorage должна содержать поле material'
        assert type(material_field) == fields.related.ForeignKey, \
            'Поле material модели MaterialStorage должно быть ссылкой ' \
            'на другую модель'
        assert material_field.related_model == Material, \
            'Поле material модели MaterialStorage должно быть ссылкой ' \
            'на модель Material'
        assert not material_field.blank, \
            'Поле material модели MaterialStorage должно быть обязательным'

        inventory_number_field = search_field(model_fields, 'inventory_number')
        assert inventory_number_field is not None, \
            'Модель MaterialStorage должна содержать поле inventory_number'
        assert type(inventory_number_field) == fields.CharField, \
            'Поле inventory_number должно быть текстовым CharField'
        assert inventory_number_field.blank, \
            'Поле inventory_number не должно быть обязательным'

        amount_field = search_field(model_fields, 'amount')
        assert amount_field is not None, \
            'Модель MaterialStorage должна содержать поле amount'
        assert type(amount_field) == fields.FloatField, \
            'Поле amount должно быть числовым FloatField'
        assert not amount_field.blank, \
            'Поле amount должно быть обязательным'

        owner_field = search_field(model_fields, 'owner_id')
        assert owner_field is not None, \
            'Модель MaterialStorage должна содержать поле owner'
        assert type(owner_field) == fields.related.ForeignKey, \
            'Поле owner должно быть ссылкой на другую модель'
        assert owner_field.related_model == Dept, \
            'Поле owner должно быть ссылкой на модель Dept'
        assert owner_field.blank, \
            'Поле owner не должно быть обязательным'

        storage_field = search_field(model_fields, 'storage_id')
        assert storage_field is not None, \
            'Модель MaterialStorage должна содержать поле storage'
        assert type(storage_field) == fields.related.ForeignKey, \
            'Поле storage должно быть ссылкой на другую модель'
        assert storage_field.related_model == Storage, \
            'Поле storage должно быть ссылкой на модель Storage'
        assert not storage_field.blank, \
            'Поле storage должно быть обязательным'
