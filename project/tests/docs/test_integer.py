import pytest
from django.db.models import IntegerField, ForeignKey, SlugField
from django.urls import reverse

from docs.forms import IntegerCreateForm, IntegerUpdateForm
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
    def test_integer_detail_view(self, client, integer):
        url = reverse('docs:integer-detail', kwargs={'pk': integer.pk})
        response = client.get(url)

        assert response.status_code == 200
        assert 'object' in response.context, \
            'Проверьте, что передали поле "object" в контекст страницы'
        assert isinstance(response.context['object'], Integer), \
            'Проверьте, что поле `object` типа Integer'
        assert response.templates[0].name == 'docs/base_element.html', \
            'Проверьте, что используете шаблон base_element.html в ответе'

    @pytest.mark.django_db
    def test_text_create_view(self, user_client, protocol):
        url = reverse('docs:integer-create')
        response = user_client.get(url)

        assert response.status_code == 200
        assert response.context.get('form'), \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], IntegerCreateForm), \
            'Проверьте, что поле `form` типа IntegerCreateForm'
        assert response.templates[0].name == 'docs/base_element.html', \
            'Проверьте, что используете шаблон base_element.html в ответе'

        data = {
            'slug': 'some-slug',
            'protocol': protocol.pk,
            'value': 12,
        }

        response = user_client.post(url, data=data, follow=True)

        assert response.status_code == 200
        assert 'object' in response.context, \
            'Проверьте, что передали поле "object" в контекст страницы'
        assert isinstance(response.context['object'], Integer), \
            'Проверьте, что поле `object` типа Integer'
        assert response.templates[0].name == 'docs/base_element.html', \
            'Проверьте, что используете шаблон base_element.html в ответе'

    @pytest.mark.django_db
    def test_integer_update_view_unautorized_user(self, client, integer):
        url = reverse('docs:integer-update', kwargs={'pk': integer.pk})
        response = client.get(url)

        assert (response.status_code in (301, 302)
                and response.url.startswith(reverse('login'))), \
            'Проверьте, что вы переадресуете пользователя на страницу авторизации'

    @pytest.mark.django_db
    def test_integer_update_view_autorized_user(self, user_client, integer):
        url = reverse('docs:integer-update', kwargs={'pk': integer.pk})
        response = user_client.get(url)

        assert response.status_code == 200
        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], IntegerUpdateForm), \
            'Проверьте, что передали поле `form` типа IntegerUpdateForm'

        data = {
            'value': 123,
        }

        response = user_client.post(url, follow=True, data=data)

        assert response.status_code == 200
        assert 'object' in response.context, \
            'Проверьте, что передали поле `object` в контекст страницы'
        assert isinstance(response.context['object'], Integer), \
            'Проверьте, что поле `object` содержит экземпляр `Integer`'
        assert data['value'] == response.context['object'].value, \
            'Проверьте, что экземпляр `Integer` был изменен'
