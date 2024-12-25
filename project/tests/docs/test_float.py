import pytest
from django.db.models import FloatField, ForeignKey, SlugField
from django.urls import reverse

from docs.forms import FloatCreateForm, FloatUpdateForm
from docs.models import Float, Protocol
from tests.common import search_field


class TestFloat:
    def test_float_model(self):
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
    def test_float_detail_view(self, client, float_):
        url = reverse('docs:float-detail', kwargs={'pk': float_.pk})
        response = client.get(url)

        assert response.status_code == 200
        assert 'object' in response.context, \
            'Проверьте, что передали поле "object" в контекст страницы'
        assert isinstance(response.context['object'], Float), \
            'Проверьте, что поле `object` типа Float'
        assert response.templates[0].name == 'docs/base_element.html', \
            'Проверьте, что используете шаблон base_element.html в ответе'

    @pytest.mark.django_db
    def test_float_create_view(self, user_client, protocol):
        url = reverse('docs:float-create')
        response = user_client.get(url)

        assert response.status_code == 200
        assert response.context.get('form'), \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], FloatCreateForm), \
            'Проверьте, что поле `form` типа FloatCreateForm'
        assert response.templates[0].name == 'docs/base_element.html', \
            'Проверьте, что используете шаблон base_element.html в ответе'

        data = {
            'slug': 'some-slug',
            'protocol': protocol.pk,
            'value': 12.2,
        }

        response = user_client.post(url, data=data, follow=True)

        assert response.status_code == 200
        assert 'object' in response.context, \
            'Проверьте, что передали поле "object" в контекст страницы'
        assert isinstance(response.context['object'], Float), \
            'Проверьте, что поле `object` типа Float'
        assert response.templates[0].name == 'docs/base_element.html', \
            'Проверьте, что используете шаблон base_element.html в ответе'

    @pytest.mark.django_db
    def test_float_update_view_unautorized_user(self, client, float_):
        url = reverse('docs:float-update', kwargs={'pk': float_.pk})
        response = client.get(url)

        assert (response.status_code in (301, 302)
                and response.url.startswith(reverse('login'))), \
            'Проверьте, что вы переадресуете пользователя на страницу авторизации'

    @pytest.mark.django_db
    def test_float_update_view_autorized_user(self, user_client, float_):
        url = reverse('docs:float-update', kwargs={'pk': float_.pk})
        response = user_client.get(url)

        assert response.status_code == 200
        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], FloatUpdateForm), \
            'Проверьте, что передали поле `form` типа FloatUpdateForm'

        data = {
            'value': 123.4,
        }

        response = user_client.post(url, follow=True, data=data)

        assert response.status_code == 200
        assert 'object' in response.context, \
            'Проверьте, что передали поле `object` в контекст страницы'
        assert isinstance(response.context['object'], Float), \
            'Проверьте, что поле `object` содержит экземпляр `Float`'
        assert data['value'] == response.context['object'].value, \
            'Проверьте, что экземпляр `Float` был изменен'
        assert response.templates[0].name == 'docs/base_element.html', \
            'Проверьте, что используете шаблон base_element.html в ответе'
