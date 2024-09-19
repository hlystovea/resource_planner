import pytest

from django.db.models.fields import CharField, IntegerField
from django.db.models.fields.related import ForeignKey
from django.urls import reverse

from hardware.forms import PartForm
from hardware.models import Cabinet, Part
from tests.common import get_field_context, search_field


class TestPart:
    test_args = ['some-name', 'foo_1', '12']

    def test_part_model(self):
        model_fields = Part._meta.fields

        name_field = search_field(model_fields, 'name')
        assert name_field is not None, \
            'Модель Part должна содержать поле name'
        assert isinstance(name_field, CharField), \
            'Поле name модели Part должно быть текстовым CharField'
        assert not name_field.blank, \
            'Поле name модели Part должно быть обязательным'

        component_field = search_field(model_fields, 'component_id')
        assert component_field is not None, \
            'Модель Part должна содержать поле function'
        assert isinstance(component_field, ForeignKey), \
            'Поле component должно быть ForeignKey'
        assert not component_field.blank, \
            'Поле component ндолжно быть обязательным'

        cabinet_field = search_field(model_fields, 'cabinet_id')
        assert cabinet_field is not None, \
            'Модель Part должна содержать поле cabinet'
        assert isinstance(cabinet_field, ForeignKey), \
            'Поле cabinet должно быть ForeignKey'
        assert not cabinet_field.blank, \
            'Поле cabinet должно быть обязательным'

        part_field = search_field(model_fields, 'part_id')
        assert part_field is not None, \
            'Модель Component должна содержать поле part'
        assert isinstance(part_field, ForeignKey), \
            'Поле part должно быть ForeignKey'
        assert part_field.blank, \
            'Поле part должно быть обязательным'

        comment_field = search_field(model_fields, 'comment')
        assert comment_field is not None, \
            'Модель Part должна содержать поле comment'
        assert isinstance(comment_field, CharField), \
            'Поле comment должно быть CharField'
        assert comment_field.blank, \
            'Поле comment не должно быть обязательным'

        release_year_field = search_field(model_fields, 'release_year')
        assert release_year_field is not None, \
            'Модель Part должна содержать поле release_year'
        assert isinstance(release_year_field, IntegerField), \
            'Поле release_year должно быть IntegerField'
        assert not release_year_field.blank, \
            'Поле release_year не должно быть обязательным'

        launch_year_field = search_field(model_fields, 'launch_year')
        assert launch_year_field is not None, \
            'Модель Part должна содержать поле launch_year'
        assert isinstance(launch_year_field, IntegerField), \
            'Поле launch_year должно быть IntegerField'
        assert not launch_year_field.blank, \
            'Поле launch_year не должно быть обязательным'

    @pytest.mark.django_db
    def test_part_view_get_detail(self, client, part):
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
            'Проверьте, что используете шаблон part_inline.html в ответе'
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
        client, _ = auto_login_user()
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

        assert 'object' in response.context, \
            'Проверьте, что передали поле "object" в контекст страницы'
        assert isinstance(response.context['object'], Part), \
            'Проверьте, что передали поле типа `Part` в контекст страницы'

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
