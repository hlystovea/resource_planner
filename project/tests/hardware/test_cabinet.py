import pytest

from django.db.models.fields import CharField, IntegerField
from django.db.models.fields.related import ForeignKey
from django.urls import reverse

from hardware.forms import CabinetForm, PartForm
from hardware.models import Cabinet, Hardware
from tests.common import get_field_context, search_field


class TestCabinet:
    test_args = ['some-name', 'foo_1', '12']

    def test_cabinet_model(self):
        model_fields = Cabinet._meta.fields

        name_field = search_field(model_fields, 'name')
        assert name_field is not None, \
            'Модель Cabinet должна содержать поле name'
        assert isinstance(name_field, CharField), \
            'Поле name модели Cabinet должно быть текстовым CharField'
        assert not name_field.blank, \
            'Поле name модели Cabinet должно быть обязательным'

        abbreviation_field = search_field(model_fields, 'abbreviation')
        assert abbreviation_field is not None, \
            'Модель Cabinet должна содержать поле abbreviation'
        assert isinstance(abbreviation_field, CharField), \
            'Поле abbreviation модели Cabinet должно быть текстовым CharField'
        assert not abbreviation_field.blank, \
            'Поле abbreviation модели Cabinet должно быть обязательным'

        hardware_field = search_field(model_fields, 'hardware_id')
        assert hardware_field is not None, \
            'Модель Cabinet должна содержать поле hardware'
        assert isinstance(hardware_field, ForeignKey), \
            'Поле hardware должно быть ForeignKey'
        assert not hardware_field.blank, \
            'Поле hardware ндолжно быть обязательным'

        manufacturer_field = search_field(model_fields, 'manufacturer_id')
        assert manufacturer_field is not None, \
            'Модель Cabinet должна содержать поле manufacturer'
        assert isinstance(manufacturer_field, ForeignKey), \
            'Поле manufacturer должно быть ForeignKey'
        assert not manufacturer_field.blank, \
            'Поле manufacturer должно быть обязательным'

        type_field = search_field(model_fields, 'type')
        assert type_field is not None, \
            'Модель Cabinet должна содержать поле type'
        assert isinstance(type_field, CharField), \
            'Поле type модели Cabinet должно быть текстовым CharField'
        assert type_field.blank, \
            'Поле type модели Cabinet не должно быть обязательным'

        series_field = search_field(model_fields, 'series')
        assert series_field is not None, \
            'Модель Cabinet должна содержать поле series'
        assert isinstance(series_field, CharField), \
            'Поле series модели Cabinet должно быть текстовым CharField'
        assert series_field.blank, \
            'Поле series модели Cabinet не должно быть обязательным'

        release_year_field = search_field(model_fields, 'release_year')
        assert release_year_field is not None, \
            'Модель Cabinet должна содержать поле release_year'
        assert isinstance(release_year_field, IntegerField), \
            'Поле release_year должно быть IntegerField'
        assert not release_year_field.blank, \
            'Поле release_year не должно быть обязательным'

        launch_year_field = search_field(model_fields, 'launch_year')
        assert launch_year_field is not None, \
            'Модель Cabinet должна содержать поле launch_year'
        assert isinstance(launch_year_field, IntegerField), \
            'Поле launch_year должно быть IntegerField'
        assert not launch_year_field.blank, \
            'Поле launch_year не должно быть обязательным'

    @pytest.mark.django_db
    def test_cabinet_view_get_detail(self, client, cabinet):
        try:
            url = reverse(
                'hardware:cabinet-detail', kwargs={'pk': cabinet.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200, \
            'Статус код страницы должен быть 200'
        assert response.templates[0].name == 'hardware/cabinet_detail.html', \
            'Проверьте, что используете шаблон cabinet_detail.html в ответе'

        cabinet = get_field_context(response.context, Cabinet)

        assert cabinet is not None, \
            'Проверьте, что передали поле типа `Cabinet` в контекст страницы'

        assert 'part_form' in response.context, \
            'Проверьте, что передали поле "part_form" в конекст страницы'
        assert isinstance(response.context['part_form'], PartForm), \
            'Проверьте, что поле "part_form" типа `PartForm`'

    @pytest.mark.django_db
    def test_cabinet_create(self, hardware, manufacturer_1, auto_login_user):
        client, _ = auto_login_user()
        url = reverse('hardware:cabinet-create')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], CabinetForm), \
            'Проверьте, что поле `form` содержит объект класса `CabinetForm`'
        assert response.templates[0].name == 'hardware/cabinet_form.html', \
            'Проверьте, что используете шаблон cabinet_form.html в ответе'

        data = {
            'name': 'some',
            'abbreviation': 'foo',
            'hardware': hardware.pk,
            'manufacturer': manufacturer_1.pk,
            'release_year': 2000,
            'launch_year': 2000,
        }

        try:
            response = client.post(url, data=data, follow=True)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'cabinet' in response.context, \
            'Проверьте, что передали поле `cabinet` в контекст страницы'
        assert isinstance(response.context['cabinet'], Cabinet), \
            'Проверьте, что поле `cabinet` содержит эксземпляр класса `Cabinet`'

        cabinet = response.context['cabinet']

        assert response.templates[0].name == 'hardware/includes/cabinet_inline.html', \
            'Проверьте, что используете шаблон cabinet_inline.html в ответе'
        assert cabinet is not None, \
            'Проверьте, что передали поле типа `Cabinet` в контекст страницы'
        assert data['name'] == cabinet.name, \
            'Проверьте, что сохраненный экземпляр `cabinet` содержит ' \
            'соответствующее поле `name`'
        assert data['abbreviation'] == cabinet.abbreviation, \
            'Проверьте, что сохраненный экземпляр `cabinet` содержит ' \
            'соответствующее поле `abbreviation`'
        assert data['hardware'] == cabinet.hardware.pk, \
            'Проверьте, что сохраненный экземпляр `cabinet` содержит ' \
            'соответствующее поле `hardware`'
        assert data['manufacturer'] == cabinet.manufacturer.pk, \
            'Проверьте, что сохраненный экземпляр `cabinet` содержит ' \
            'соответствующее поле `manufacturer`'
        assert data['release_year'] == cabinet.release_year, \
            'Проверьте, что сохраненный экземпляр `cabinet` содержит ' \
            'соответствующее поле `release_year`'
        assert data['launch_year'] == cabinet.launch_year, \
            'Проверьте, что сохраненный экземпляр `cabinet` содержит ' \
            'соответствующее поле `launch_year`'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name', test_args)
    def test_cabinet_view_update(self, name, auto_login_user, cabinet):
        client, _ = auto_login_user()
        url = reverse(
            'hardware:cabinet-update',
            kwargs={'pk': cabinet.pk}
        )

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], CabinetForm), \
            'Проверьте, что поле `form` содержит объект класса `CabinetForm`'

        data = {
            'name': name,
        }

        try:
            response = client.post(url, follow=True, data=data)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        cabinet = get_field_context(response.context, Cabinet)

        assert cabinet is not None, \
            'Проверьте, что передали поле типа Cabinet в контекст страницы'
        assert data['name'] == cabinet.name, \
            'Проверьте, что сохраненный экземпляр `cabinet` содержит' \
            'соответствующее поле `name`'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name', test_args)
    def test_cabinet_view_delete(
        self, name, hardware, manufacturer_1, auto_login_user
    ):
        client, _ = auto_login_user()
        cabinet = Cabinet.objects.create(
            name=name,
            abbreviation=name,
            hardware=hardware,
            manufacturer=manufacturer_1,
            release_year=2000,
            launch_year=2000
        )
        queryset = Cabinet.objects.filter(name=name)

        assert queryset.exists(), \
            'Тест работает неправильно, экземпляр `cabinet` отсутствует в БД'

        url = reverse('hardware:cabinet-delete', kwargs={'pk': cabinet.pk})

        try:
            response = client.delete(url, follow=True)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert not queryset.exists(), \
            'Проверьте, что эксземпляр `cabinet` удаляется из БД'

    @pytest.mark.django_db
    def test_cabinet_view_get_inline(self, client, cabinet):
        try:
            url = reverse(
                'hardware:cabinet-inline', kwargs={'pk': cabinet.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200, \
            'Статус код страницы должен быть 200'
        assert response.templates[0].name == 'hardware/includes/cabinet_inline.html', \
            'Проверьте, что используете шаблон cabinet_inline.html в ответе'

        assert 'cabinet' in response.context, \
            'Проверьте, что передали поле cabinet в контекст страницы'
        assert isinstance(response.context['cabinet'], Cabinet), \
            'Проверьте, что передали поле типа `Cabinet` в контекст страницы'

    @pytest.mark.django_db
    def test_cabinet_view_get_li(self, client, cabinet):
        try:
            url = reverse(
                'hardware:cabinet-li', kwargs={'pk': cabinet.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200, \
            'Статус код страницы должен быть 200'
        assert response.templates[0].name == 'hardware/includes/menu_li.html', \
            'Проверьте, что используете шаблон menu_li.html в ответе'

        assert 'object' in response.context, \
            'Проверьте, что передали поле "object" в контекст страницы'
        assert isinstance(response.context['object'], Cabinet), \
            'Проверьте, что передали поле типа `Cabinet` в контекст страницы'

    @pytest.mark.django_db
    def test_cabinet_view_get_ul(self, client, hardware):
        try:
            url = reverse(
                'hardware:cabinet-ul', kwargs={'pk': hardware.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200, \
            'Статус код страницы должен быть 200'
        assert response.templates[0].name == 'hardware/includes/menu_ul.html', \
            'Проверьте, что используете шаблон menu_ul.html в ответе'

        assert 'object' in response.context, \
            'Проверьте, что передали поле object в контекст страницы'
        assert isinstance(response.context['object'], Hardware), \
            'Проверьте, что передали поле типа `Hardware` в контекст страницы'

    @pytest.mark.django_db
    def test_cabinet_view_get_select(self, client):
        url = reverse('hardware:cabinet-select')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'cabinet_list' in response.context, \
            'Проверьте, что передали поле "cabinet_list" в контекст страницы'
        assert response.templates[0].name == 'hardware/includes/cabinet_select.html', \
            'Проверьте, что используете шаблон cabinet_select.html в ответе'
