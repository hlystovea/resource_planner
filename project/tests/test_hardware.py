import pytest

from django.db.models import fields
from django.urls import reverse

from hardware.forms import ComponentForm, PartForm
from hardware.models import Cabinet, Component, Part
from tests.common import get_field_context, search_field
from warehouse.models import ComponentStorage


class TestComponent:
    test_args = ['some-name', 'foo_1', '12']

    def test_component_model(self):
        model_fields = Component._meta.fields

        name_field = search_field(model_fields, 'name')
        assert name_field is not None, \
            'Модель Component должна содержать поле name'
        assert type(name_field) == fields.CharField, \
            'Поле name модели Component должно быть текстовым CharField'
        assert not name_field.blank, \
            'Поле name модели Component должно быть обязательным'

        function_field = search_field(model_fields, 'function_id')
        assert function_field is not None, \
            'Модель Component должна содержать поле function'
        assert type(function_field) == fields.related.ForeignKey, \
            'Поле function должно быть ForeignKey'
        assert not function_field.blank, \
            'Поле function ндолжно быть обязательным'

        design_field = search_field(model_fields, 'design_id')
        assert design_field is not None, \
            'Модель Component должна содержать поле design'
        assert type(design_field) == fields.related.ForeignKey, \
            'Поле design должно быть ForeignKey'
        assert not design_field.blank, \
            'Поле design должно быть обязательным'

        manufacturer_field = search_field(model_fields, 'manufacturer_id')
        assert manufacturer_field is not None, \
            'Модель Component должна содержать поле manufacturer'
        assert type(manufacturer_field) == fields.related.ForeignKey, \
            'Поле manufacturer должно быть ForeignKey'
        assert not manufacturer_field.blank, \
            'Поле manufacturer должно быть обязательным'

        type_field = search_field(model_fields, 'type')
        assert type_field is not None, \
            'Модель Component должна содержать поле type'
        assert type(type_field) == fields.CharField, \
            'Поле type должно быть CharField'
        assert type_field.blank, \
            'Поле type не должно быть обязательным'

        series_field = search_field(model_fields, 'series')
        assert series_field is not None, \
            'Модель Component должна содержать поле series'
        assert type(series_field) == fields.CharField, \
            'Поле series должно быть CharField'
        assert series_field.blank, \
            'Поле series не должно быть обязательным'

    @pytest.mark.django_db
    def test_component_view_get_list(self, client):
        url = reverse('hardware:component-list')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200
        assert response.templates[0].name == 'hardware/component_list.html', \
            'Проверьте, что используете шаблон component_list.html в ответе'

        assert 'component_list' in response.context, \
            'Проверьте, что передали поле "component_list" в контекст страницы'

    @pytest.mark.django_db
    def test_component_view_get_detail(
        self, client, component_1, component_in_storage_dept1
    ):
        try:
            url = reverse(
                'hardware:component-detail', kwargs={'pk': component_1.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200, \
            'Статус код страницы должен быть 200'
        assert response.templates[0].name == 'hardware/component_detail.html', \
            'Проверьте, что используете шаблон component_detail.html в ответе'

        component = get_field_context(response.context, Component)

        assert component is not None, \
            'Проверьте, что передали поле типа `Component` в контекст страницы'
        assert type(component.amount.first()) == ComponentStorage, \
            'Проверьте, что вместе с объектом Component передали поле ' \
            'типа ComponentStorage в контекст страницы'

        assert component.in_storage == component_in_storage_dept1.amount, \
            'Проверьте, что объект Component содержит поле in_storage ' \
            'с общим количеством материала'

        assert component.in_hardware == component_in_storage_dept1.component.parts.count(), \
            'Проверьте, что объект Component содержит поле in_hardware ' \
            'с общим количеством оборудования'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name', test_args)
    def test_component_view_create(
        self, name, function, design, manufacturer_1, auto_login_user
    ):
        client, user = auto_login_user()
        url = reverse('hardware:component-create')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200
        assert response.templates[0].name == 'hardware/component_form.html', \
            'Проверьте, что используете шаблон component_form.html в ответе'

        form = get_field_context(response.context, ComponentForm)

        assert form is not None, \
            'Проверьте, что передали поле типа `ComponentForm` в контекст стр.'
        assert 'is_new' in response.context, \
            'Проверьте, что передали поле `is_new` в контекст страницы'
        assert response.context['is_new'], \
            'Проверьте, что значение поля `is_new` в контексте стр. = `True`'

        data = {
            'name': name,
            'function': function,
            'design': design,
            'manufacturer': manufacturer_1
        }
        try:
            response = client.post(url, follow=True, data=data)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

    @pytest.mark.django_db
    @pytest.mark.parametrize('name', test_args)
    def test_component_view_create_modal(
        self, name, function, design, manufacturer_1, auto_login_user
    ):
        client, user = auto_login_user()
        url = reverse('hardware:component-create-modal')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200
        assert response.templates[0].name == 'hardware/includes/component_form_modal.html', \
            'Проверьте, что используете шаблон component_form_modal.html в ответе'

        form = get_field_context(response.context, ComponentForm)

        assert form is not None, \
            'Проверьте, что передали поле типа `ComponentForm` в контекст стр.'

        data = {
            'name': name,
            'function': function,
            'design': design,
            'manufacturer': manufacturer_1
        }
        try:
            response = client.post(url, follow=True, data=data)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

    @pytest.mark.django_db
    @pytest.mark.parametrize('name', test_args)
    def test_component_view_update(self, name, auto_login_user, component_1):
        client, user = auto_login_user()
        url = reverse(
            'hardware:component-update',
            kwargs={'pk': component_1.pk}
        )

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], ComponentForm), \
            'Проверьте, что поле `form` содержит объект класса `ComponentForm`'

        data = {
            'name': name,
        }
        try:
            response = client.post(url, follow=True, data=data)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        component = get_field_context(response.context, Component)

        assert component is not None, \
            'Проверьте, что передали поле типа Component в контекст страницы'
        assert data['name'] == component.name, \
            'Проверьте, что сохраненный экземпляр `component` содержит' \
            'соответствующее поле `name`'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name', test_args)
    def test_component_view_delete(
        self, name, function, design, auto_login_user
    ):
        client, user = auto_login_user()
        component = Component.objects.create(
            name=name,
            function=function,
            design=design
        )
        queryset = Component.objects.filter(name=name)

        assert queryset.exists(), \
            'Тест работает неправильно, экземпляр `component` отсутствует в БД'

        url = reverse('hardware:component-delete', kwargs={'pk': component.pk})

        try:
            response = client.delete(url, follow=True)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert not queryset.exists(), \
            'Проверьте, что эксземпляр `component` удаляется из БД'

    @pytest.mark.django_db
    def test_component_filters(
        self, client, component_in_storage_dept1, component_in_storage_dept2
    ):
        url = reverse('hardware:component-list')
        components = Component.objects.all()

        response = client.get(url)
        component_list = response.context['component_list']

        assert len(component_list) == len(components), \
            'Проверьте, что без фильтрации передаются все объекты'

        response = client.get(f'{url}?dept={component_in_storage_dept1.storage.owner.pk}')
        component_list = response.context['component_list']

        assert component_in_storage_dept1.component in component_list, \
            'Фильтр по подразделению работает не правильно'
        assert component_in_storage_dept2.component not in component_list, \
            'Фильтр по подразделению работает не правильно'

        manufacturer_1 = component_in_storage_dept1.component.manufacturer
        response = client.get(f'{url}?manufacturer={manufacturer_1.pk}')
        component_list = response.context['component_list']

        assert component_in_storage_dept1.component in component_list, \
            'Фильтр по производителю работает не правильно'
        assert component_in_storage_dept2.component not in component_list, \
            'Фильтр по производителю работает не правильно'

    @pytest.mark.django_db
    def test_defect_count_in_component_list(
        self, client, part, component_1, defect
    ):
        part_2 = part
        part_2.pk = None
        part_2.name = 'another'
        part_2.save()

        defect.pk = None
        defect.part = part_2
        defect.save()

        url = reverse(
            'hardware:component-detail',
            kwargs={'pk': component_1.pk}
        )

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        component = get_field_context(response.context, Component)

        assert component.defect_count == 2, \
            'Проверьте, что объект Component содержит поле defect_count ' \
            'с количеством дефектов'

    @pytest.mark.django_db
    def test_component_view_get_select(self, client):
        url = reverse('hardware:component-select')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'component_list' in response.context, \
            'Проверьте, что передали поле "component_list" в контекст страницы'
        assert response.templates[0].name == 'hardware/includes/component_select.html', \
            'Проверьте, что используете шаблон component_select.html в ответе'


class TestPart:
    test_args = ['some-name', 'foo_1', '12']

    def test_component_model(self):
        model_fields = Part._meta.fields

        name_field = search_field(model_fields, 'name')
        assert name_field is not None, \
            'Модель Part должна содержать поле name'
        assert type(name_field) == fields.CharField, \
            'Поле name модели Part должно быть текстовым CharField'
        assert not name_field.blank, \
            'Поле name модели Part должно быть обязательным'

        component_field = search_field(model_fields, 'component_id')
        assert component_field is not None, \
            'Модель Part должна содержать поле function'
        assert type(component_field) == fields.related.ForeignKey, \
            'Поле component должно быть ForeignKey'
        assert not component_field.blank, \
            'Поле component ндолжно быть обязательным'

        cabinet_field = search_field(model_fields, 'cabinet_id')
        assert cabinet_field is not None, \
            'Модель Part должна содержать поле cabinet'
        assert type(cabinet_field) == fields.related.ForeignKey, \
            'Поле cabinet должно быть ForeignKey'
        assert not cabinet_field.blank, \
            'Поле cabinet должно быть обязательным'

        part_field = search_field(model_fields, 'part_id')
        assert part_field is not None, \
            'Модель Component должна содержать поле part'
        assert type(part_field) == fields.related.ForeignKey, \
            'Поле part должно быть ForeignKey'
        assert part_field.blank, \
            'Поле part должно быть обязательным'

        comment_field = search_field(model_fields, 'comment')
        assert comment_field is not None, \
            'Модель Part должна содержать поле comment'
        assert type(comment_field) == fields.CharField, \
            'Поле comment должно быть CharField'
        assert comment_field.blank, \
            'Поле comment не должно быть обязательным'

        release_year_field = search_field(model_fields, 'release_year')
        assert release_year_field is not None, \
            'Модель Part должна содержать поле release_year'
        assert type(release_year_field) == fields.IntegerField, \
            'Поле release_year должно быть IntegerField'
        assert not release_year_field.blank, \
            'Поле release_year не должно быть обязательным'

        launch_year_field = search_field(model_fields, 'launch_year')
        assert launch_year_field is not None, \
            'Модель Part должна содержать поле launch_year'
        assert type(launch_year_field) == fields.IntegerField, \
            'Поле launch_year должно быть IntegerField'
        assert not launch_year_field.blank, \
            'Поле launch_year не должно быть обязательным'

    @pytest.mark.django_db
    def test_component_view_get_detail(self, client, part):
        try:
            url = reverse(
                'hardware:part-detail', kwargs={'pk': part.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200, \
            'Статус код страницы должен быть 200'
        assert response.templates[0].name == 'hardware/part_detail.html', \
            'Проверьте, что используете шаблон part_detail.html в ответе'

        part = get_field_context(response.context, Part)

        assert part is not None, \
            'Проверьте, что передали поле типа `Part` в контекст страницы'

        form = get_field_context(response.context, PartForm)

        assert form is not None, \
            'Проверьте, что передали поле типа `PartForm` в контекст стр.'

    @pytest.mark.django_db
    def test_part_create(self, component_1, cabinet, auto_login_user):
        client, user = auto_login_user()
        url = reverse('hardware:part-create')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], PartForm), \
            'Проверьте, что поле `form` содержит объект класса `PartForm`'
        assert response.templates[0].name == 'hardware/part_form.html', \
            'Проверьте, что используете шаблон part_form.html в ответе'

        data = {
            'name': 'some',
            'component': component_1.pk,
            'cabinet': cabinet.pk,
            'release_year': 2000,
            'launch_year': 2000,
        }
        try:
            response = client.post(url, data=data, follow=True)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'part' in response.context, \
            'Проверьте, что передали поле `part` в контекст страницы'
        assert isinstance(response.context['part'], Part), \
            'Проверьте, что поле `part` содержит эксземпляр класса `Part`'

        part = response.context['part']

        assert response.templates[0].name == 'hardware/includes/part_inline.html', \
            'Проверьте, что используете шаблон part_create_success_modal.html в ответе'
        assert part is not None, \
            'Проверьте, что передали поле типа `Part` в контекст страницы'
        assert data['name'] == part.name, \
            'Проверьте, что сохраненный экземпляр `part` содержит ' \
            'соответствующее поле `name`'
        assert data['cabinet'] == part.cabinet.pk, \
            'Проверьте, что сохраненный экземпляр `part` содержит ' \
            'соответствующее поле `cabinet`'

    @pytest.mark.django_db
    def test_part_create_modal(self, component_1, cabinet, auto_login_user):
        client, user = auto_login_user()
        url = reverse('hardware:part-create-modal')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], PartForm), \
            'Проверьте, что поле `form` содержит объект класса `PartForm`'
        assert response.templates[0].name == 'hardware/includes/part_form_modal.html', \
            'Проверьте, что используете шаблон part_form_modal.html в ответе'

        data = {
            'name': 'some',
            'component': component_1.pk,
            'cabinet': cabinet.pk,
            'release_year': 2000,
            'launch_year': 2000,
        }
        try:
            response = client.post(url, data=data)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'part' in response.context, \
            'Проверьте, что передали поле `part` в контекст страницы'
        assert isinstance(response.context['part'], Part), \
            'Проверьте, что поле `part` содержит эксземпляр класса `Part`'

        part = response.context['part']

        assert response.templates[0].name == 'hardware/includes/part_create_success_modal.html', \
            'Проверьте, что используете шаблон part_create_success_modal.html в ответе'
        assert part is not None, \
            'Проверьте, что передали поле типа `Part` в контекст страницы'
        assert data['name'] == part.name, \
            'Проверьте, что сохраненный экземпляр `part` содержит ' \
            'соответствующее поле `name`'
        assert data['cabinet'] == part.cabinet.pk, \
            'Проверьте, что сохраненный экземпляр `part` содержит ' \
            'соответствующее поле `cabinet`'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name', test_args)
    def test_part_view_update(self, name, auto_login_user, part):
        client, _ = auto_login_user()
        url = reverse(
            'hardware:part-update',
            kwargs={'pk': part.pk}
        )

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], PartForm), \
            'Проверьте, что поле `form` содержит объект класса `PartForm`'

        data = {
            'name': name,
        }
        try:
            response = client.post(url, follow=True, data=data)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        part = get_field_context(response.context, Part)

        assert part is not None, \
            'Проверьте, что передали поле типа Part в контекст страницы'
        assert data['name'] == part.name, \
            'Проверьте, что сохраненный экземпляр `part` содержит' \
            'соответствующее поле `name`'

    @pytest.mark.django_db
    @pytest.mark.parametrize('name', test_args)
    def test_part_view_delete(
        self, name, component_1, cabinet, auto_login_user
    ):
        client, _ = auto_login_user()
        part = Part.objects.create(
            name=name,
            component=component_1,
            cabinet=cabinet,
            release_year=2000,
            launch_year=2000
        )
        queryset = Part.objects.filter(name=name)

        assert queryset.exists(), \
            'Тест работает неправильно, экземпляр `part` отсутствует в БД'

        url = reverse('hardware:part-delete', kwargs={'pk': part.pk})

        try:
            response = client.delete(url, follow=True)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert not queryset.exists(), \
            'Проверьте, что эксземпляр `part` удаляется из БД'

    @pytest.mark.django_db
    def test_part_view_get_inline(self, client, part):
        try:
            url = reverse(
                'hardware:part-inline', kwargs={'pk': part.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200, \
            'Статус код страницы должен быть 200'
        assert response.templates[0].name == 'hardware/includes/part_inline.html', \
            'Проверьте, что используете шаблон part_inline.html в ответе'

        assert 'part' in response.context, \
            'Проверьте, что передали поле part в контекст страницы'
        assert isinstance(response.context['part'], Part), \
            'Проверьте, что передали поле типа `Part` в контекст страницы'

    @pytest.mark.django_db
    def test_part_view_get_li(self, client, part):
        try:
            url = reverse(
                'hardware:part-li', kwargs={'pk': part.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200, \
            'Статус код страницы должен быть 200'
        assert response.templates[0].name == 'hardware/includes/menu_li.html', \
            'Проверьте, что используете шаблон menu_li.html в ответе'

        assert 'object' in response.context, \
            'Проверьте, что передали поле part в контекст страницы'
        assert isinstance(response.context['object'], Part), \
            'Проверьте, что передали поле типа `Part` в контекст страницы'

    @pytest.mark.django_db
    def test_part_view_get_ul(self, client, part):
        try:
            url = reverse(
                'hardware:part-ul', kwargs={'pk': part.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200, \
            'Статус код страницы должен быть 200'
        assert response.templates[0].name == 'hardware/includes/menu_ul.html', \
            'Проверьте, что используете шаблон menu_ul.html в ответе'

        object = get_field_context(response.context, Cabinet)

        assert object is not None, \
            'Проверьте, что передали поле типа `Cabinet` в контекст страницы'

    @pytest.mark.django_db
    def test_part_view_get_select(self, client):
        url = reverse('hardware:part-select')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'part_list' in response.context, \
            'Проверьте, что передали поле "part_list" в контекст страницы'
        assert response.templates[0].name == 'hardware/includes/part_select.html', \
            'Проверьте, что используете шаблон part_select.html в ответе'
