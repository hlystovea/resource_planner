import pytest
from django.db.models import FloatField, ForeignKey, SlugField
from django.urls import reverse

from docs.forms import FloatForm
from docs.models import Float, Protocol
from tests.common import search_field


class TestFloat:
    def test_text_model(self):
        model_fields = Float._meta.fields

        slug_field = search_field(model_fields, 'slug')
        assert slug_field is not None, \
            'Модель Float должна содержать поле "slug"'
        assert isinstance(slug_field, SlugField), \
            'Поле "slug" модели Float должно быть SlugField'
        assert not slug_field.blank, \
            'Поле "slug" модели Float должно быть обязательным'

        protocol_field = search_field(model_fields, 'protocol_id')
        assert protocol_field is not None, \
            'Модель Float должна содержать поле "protocol"'
        assert isinstance(protocol_field, ForeignKey), \
            'Поле "protocol" модели Float должно быть ForeignKey'
        assert protocol_field.related_model == Protocol, \
            'Поле protocol модели Float должно быть ссылкой на модель Protocol'
        assert not protocol_field.blank, \
            'Поле "protocol" модели Float должно быть обязательным'

        value_field = search_field(model_fields, 'value')
        assert value_field is not None, \
            'Модель Float должна содержать поле "value"'
        assert isinstance(value_field, FloatField), \
            'Поле "value" модели Float должно быть FloatField'
        assert not value_field.blank, \
            'Поле "value" модели Float должно быть обязательным'

    @pytest.mark.django_db
    def test_text_create_view(self, user_client, protocol):
        url = reverse('docs:float-create')
        response = user_client.get(url)

        assert response.status_code == 200
        assert response.context.get('form'), \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], FloatForm), \
            'Проверьте, что поле `form` типа FloatForm'
        assert response.templates[0].name == 'docs/includes/base_element.html', \
            'Проверьте, что используете шаблон base_element.html в ответе'

        data = {
            'slug': 'some-slug',
            'protocol': protocol.pk,
            'value': 12.2,
        }

        response = user_client.post(url, data=data, follow=True)

        assert response.status_code == 200
        assert response.templates[0].name == 'docs/includes/base_element.html', \
            'Проверьте, что используете шаблон base_element.html в ответе'
