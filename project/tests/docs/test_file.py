import pytest
from django.db.models import FileField, ForeignKey, SlugField
from django.urls import reverse

from docs.forms import ImageForm
from docs.models import File, Protocol
from tests.common import search_field


class TestFile:
    def test_file_model(self):
        model_fields = File._meta.fields

        slug_field = search_field(model_fields, 'slug')
        assert slug_field is not None, \
            'Модель File должна содержать поле "slug"'
        assert isinstance(slug_field, SlugField), \
            'Поле "slug" модели File должно быть SlugField'
        assert not slug_field.blank, \
            'Поле "slug" модели File должно быть обязательным'

        protocol_field = search_field(model_fields, 'protocol_id')
        assert protocol_field is not None, \
            'Модель File должна содержать поле "protocol"'
        assert isinstance(protocol_field, ForeignKey), \
            'Поле "protocol" модели File должно быть ForeignKey'
        assert protocol_field.related_model == Protocol, \
            'Поле protocol модели File должно быть ссылкой на модель Protocol'
        assert not protocol_field.blank, \
            'Поле "protocol" модели File должно быть обязательным'

        value_field = search_field(model_fields, 'value')
        assert value_field is not None, \
            'Модель File должна содержать поле "value"'
        assert isinstance(value_field, FileField), \
            'Поле "value" модели File должно быть FileField'
        assert not value_field.blank, \
            'Поле "value" модели File должно быть обязательным'

    @pytest.mark.django_db
    def test_image_create_view(self, user_client, protocol):
        url = reverse('docs:image-create')
        response = user_client.get(url)

        assert response.status_code == 200
        assert response.context.get('form'), \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], ImageForm), \
            'Проверьте, что поле `form` типа TextForm'
        assert response.templates[0].name == 'docs/includes/image_element.html', \
            'Проверьте, что используете шаблон image_element.html в ответе'

        data = {
            'slug': 'some-slug',
            'protocol': protocol.pk,
            'value': 'Some value',
        }

        response = user_client.post(url, data=data, follow=True)

        assert response.status_code == 200
        assert response.templates[0].name == 'docs/includes/image_element.html', \
            'Проверьте, что используете шаблон image_element.html в ответе'
