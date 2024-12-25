import pytest
from django.db.models import TextField, ForeignKey, SlugField
from django.urls import reverse

from docs.forms import (CharCreateForm, CharUpdateForm,
                        TextCreateForm, TextUpdateForm)
from docs.models import Text, Protocol
from tests.common import search_field


class TestText:
    def test_text_model(self):
        model_fields = Text._meta.fields

        slug_field = search_field(model_fields, 'slug')
        assert slug_field is not None, \
            'Модель Text должна содержать поле "slug"'
        assert isinstance(slug_field, SlugField), \
            'Поле "slug" модели Text должно быть SlugField'
        assert not slug_field.blank, \
            'Поле "slug" модели Text должно быть обязательным'

        protocol_field = search_field(model_fields, 'protocol_id')
        assert protocol_field is not None, \
            'Модель Text должна содержать поле "protocol"'
        assert isinstance(protocol_field, ForeignKey), \
            'Поле "protocol" модели Text должно быть ForeignKey'
        assert protocol_field.related_model == Protocol, \
            'Поле protocol модели Text должно быть ссылкой на модель Protocol'
        assert not protocol_field.blank, \
            'Поле "protocol" модели Text должно быть обязательным'

        value_field = search_field(model_fields, 'value')
        assert value_field is not None, \
            'Модель Text должна содержать поле "value"'
        assert isinstance(value_field, TextField), \
            'Поле "value" модели Text должно быть TextField'
        assert not value_field.blank, \
            'Поле "value" модели Text должно быть обязательным'

    @pytest.mark.django_db
    def test_text_detail_view(self, client, text):
        url = reverse('docs:text-detail', kwargs={'pk': text.pk})
        response = client.get(url)

        assert response.status_code == 200
        assert 'object' in response.context, \
            'Проверьте, что передали поле "object" в контекст страницы'
        assert isinstance(response.context['object'], Text), \
            'Проверьте, что поле `object` содержит экземпляр `Text`'
        assert response.templates[0].name == 'docs/text_element.html', \
            'Проверьте, что используете шаблон text_element.html в ответе'

    @pytest.mark.django_db
    def test_text_create_view(self, user_client, protocol):
        url = reverse('docs:text-create')
        response = user_client.get(url)

        assert response.status_code == 200
        assert response.context.get('form'), \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], TextCreateForm), \
            'Проверьте, что поле `form` типа TextCreateForm'
        assert response.templates[0].name == 'docs/text_element.html', \
            'Проверьте, что используете шаблон text_element.html в ответе'

        data = {
            'slug': 'some-slug',
            'protocol': protocol.pk,
            'value': 'Some value',
        }

        response = user_client.post(url, data=data, follow=True)

        assert response.status_code == 200
        assert 'object' in response.context, \
            'Проверьте, что передали поле "object" в контекст страницы'
        assert isinstance(response.context['object'], Text), \
            'Проверьте, что поле `object` содержит экземпляр `Text`'
        assert response.templates[0].name == 'docs/text_element.html', \
            'Проверьте, что используете шаблон text_element.html в ответе'

    @pytest.mark.django_db
    def test_text_update_view_unautorized_user(self, client, text):
        url = reverse('docs:text-update', kwargs={'pk': text.pk})
        response = client.get(url)

        assert (response.status_code in (301, 302)
                and response.url.startswith(reverse('login'))), \
            'Проверьте, что вы переадресуете пользователя на страницу авторизации'

    @pytest.mark.django_db
    def test_text_update_view_autorized_user(self, user_client, text):
        url = reverse('docs:text-update', kwargs={'pk': text.pk})
        response = user_client.get(url)

        assert response.status_code == 200
        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], TextUpdateForm), \
            'Проверьте, что передали поле `form` типа TextUpdateForm'
        assert response.templates[0].name == 'docs/text_element.html', \
            'Проверьте, что используете шаблон text_element.html в ответе'

        data = {
            'value': 'foo-bar',
        }

        response = user_client.post(url, follow=True, data=data)

        assert response.status_code == 200
        assert 'object' in response.context, \
            'Проверьте, что передали поле `object` в контекст страницы'
        assert isinstance(response.context['object'], Text), \
            'Проверьте, что поле `object` содержит экземпляр `Text`'
        assert data['value'] == response.context['object'].value, \
            'Проверьте, что экземпляр `Text` был изменен'
        assert response.templates[0].name == 'docs/text_element.html', \
            'Проверьте, что используете шаблон text_element.html в ответе'

    @pytest.mark.django_db
    def test_char_detail_view(self, client, char):
        url = reverse('docs:char-detail', kwargs={'pk': char.pk})
        response = client.get(url)

        assert response.status_code == 200
        assert 'object' in response.context, \
            'Проверьте, что передали поле "object" в контекст страницы'
        assert isinstance(response.context['object'], Text), \
            'Проверьте, что поле `object` содержит экземпляр `Text`'
        assert response.templates[0].name == 'docs/base_element.html', \
            'Проверьте, что используете шаблон base_element.html в ответе'

    @pytest.mark.django_db
    def test_char_create_view(self, user_client, protocol):
        url = reverse('docs:char-create')
        response = user_client.get(url)

        assert response.status_code == 200
        assert response.context.get('form'), \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], CharCreateForm), \
            'Проверьте, что поле `form` типа CharCreateForm'
        assert response.templates[0].name == 'docs/base_element.html', \
            'Проверьте, что используете шаблон base_element.html в ответе'

        data = {
            'slug': 'some-slug',
            'protocol': protocol.pk,
            'value': 'Some value',
        }

        response = user_client.post(url, data=data, follow=True)

        assert response.status_code == 200
        assert 'object' in response.context, \
            'Проверьте, что передали поле "object" в контекст страницы'
        assert isinstance(response.context['object'], Text), \
            'Проверьте, что поле `object` содержит экземпляр `Text`'
        assert response.templates[0].name == 'docs/base_element.html', \
            'Проверьте, что используете шаблон base_element.html в ответе'

    @pytest.mark.django_db
    def test_char_update_view_unautorized_user(self, client, char):
        url = reverse('docs:char-update', kwargs={'pk': char.pk})
        response = client.get(url)

        assert (response.status_code in (301, 302)
                and response.url.startswith(reverse('login'))), \
            'Проверьте, что вы переадресуете пользователя на страницу авторизации'

    @pytest.mark.django_db
    def test_char_update_view_autorized_user(self, user_client, char):
        url = reverse('docs:char-update', kwargs={'pk': char.pk})
        response = user_client.get(url)

        assert response.status_code == 200
        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], CharUpdateForm), \
            'Проверьте, что передали поле `form` типа CharUpdateForm'
        assert response.templates[0].name == 'docs/base_element.html', \
            'Проверьте, что используете шаблон base_element.html в ответе'

        data = {
            'value': 'foo-bar',
        }

        response = user_client.post(url, follow=True, data=data)

        assert response.status_code == 200
        assert 'object' in response.context, \
            'Проверьте, что передали поле `object` в контекст страницы'
        assert isinstance(response.context['object'], Text), \
            'Проверьте, что поле `object` содержит экземпляр `Text`'
        assert data['value'] == response.context['object'].value, \
            'Проверьте, что экземпляр `Text` был изменен'
        assert response.templates[0].name == 'docs/base_element.html', \
            'Проверьте, что используете шаблон base_element.html в ответе'
