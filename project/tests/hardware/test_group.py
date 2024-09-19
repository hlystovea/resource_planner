import pytest

from django.db.models.fields import CharField
from django.urls import reverse

from hardware.models import Group
from tests.common import search_field


class TestGroup:
    def test_group_model(self):
        model_fields = Group._meta.fields

        name_field = search_field(model_fields, 'name')
        assert name_field is not None, \
            'Модель Group должна содержать поле name'
        assert isinstance(name_field, CharField), \
            'Поле name модели Group должно быть текстовым CharField'
        assert not name_field.blank, \
            'Поле name модели Group должно быть обязательным'

    @pytest.mark.django_db
    def test_group_view_get_select(self, client):
        url = reverse('hardware:group-select')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'group_list' in response.context, \
            'Проверьте, что передали поле "group_list" в контекст страницы'
        assert response.templates[0].name == 'hardware/includes/group_select.html', \
            'Проверьте, что используете шаблон group_select.html в ответе'
