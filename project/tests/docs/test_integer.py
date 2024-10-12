import pytest
from django.db.models import IntegerField, ForeignKey, SlugField
from django.urls import reverse

from docs.forms import IntegerForm
from docs.models import Integer, Protocol
from tests.common import search_field


class TestInteger:
    def test_text_model(self):
        model_fields = Integer._meta.fields

        slug_field = search_field(model_fields, 'slug')
        assert slug_field is not None, \
            'Модель Integer должна содержать поле "slug"'
        assert isinstance(slug_field, SlugField), \
            'Поле "slug" модели Integer должно быть SlugField'
        assert not slug_field.blank, \
            'Поле "slug" модели Integer должно быть обязательным'

        protocol_field = search_field(model_fields, 'protocol_id')
        assert protocol_field is not None, \
            'Модель Integer должна содержать поле "protocol"'
        assert isinstance(protocol_field, ForeignKey), \
            'Поле "protocol" модели Integer должно быть ForeignKey'
        assert protocol_field.related_model == Protocol, \
            'Поле protocol модели Integer должно быть ссылкой на модель Protocol'
        assert not protocol_field.blank, \
            'Поле "protocol" модели Integer должно быть обязательным'

        value_field = search_field(model_fields, 'value')
        assert value_field is not None, \
            'Модель Integer должна содержать поле "value"'
        assert isinstance(value_field, IntegerField), \
            'Поле "value" модели Integer должно быть IntegerField'
        assert not value_field.blank, \
            'Поле "value" модели Integer должно быть обязательным'

    @pytest.mark.django_db
    def test_text_create_view(self, user_client, protocol):
        url = reverse('docs:integer-create')
        response = user_client.get(url)

        assert response.status_code == 200
        assert response.context.get('form'), \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], IntegerForm), \
            'Проверьте, что поле `form` типа IntegerForm'
        assert response.templates[0].name == 'docs/includes/base_element.html', \
            'Проверьте, что используете шаблон base_element.html в ответе'

        data = {
            'slug': 'some-slug',
            'protocol': protocol.pk,
            'value': 12,
        }

        response = user_client.post(url, data=data, follow=True)

        assert response.status_code == 200
        assert response.templates[0].name == 'docs/includes/base_element.html', \
            'Проверьте, что используете шаблон base_element.html в ответе'
