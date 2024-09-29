import pytest
from django.db.models import CharField, FileField
from django.urls import reverse

from docs.models import Template
from tests.common import search_field


class TestTemplate:
    def test_template_model(self):
        model_fields = Template._meta.fields

        name_field = search_field(model_fields, 'name')
        assert name_field is not None, \
            'Модель Template должна содержать поле "name"'
        assert isinstance(name_field, CharField), \
            'Поле "name" модели Template должно быть CharField'
        assert not name_field.blank, \
            'Поле "name" модели Template должно быть обязательным'

        file_field = search_field(model_fields, 'file')
        assert file_field is not None, \
            'Модель Template должна содержать поле "file"'
        assert isinstance(file_field, FileField), \
            'Поле "file" модели Template должно быть FileField'
        assert not file_field.blank, \
            'Поле "file" модели Template должно быть обязательным'

    @pytest.mark.django_db
    def test_template_select_view(self, client):
        url = reverse('docs:template-select')

        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'
        assert response.status_code == 200

        assert 'template_list' in response.context, \
            'Проверьте, что передали поле "template_list" в контекст страницы'
        assert response.templates[0].name == 'docs/includes/template_select.html', \
            'Проверьте, что используете шаблон template_select.html в ответе'
