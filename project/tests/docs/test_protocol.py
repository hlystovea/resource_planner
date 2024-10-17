import pytest
from django.db.models import DateField, ForeignKey
from django.db.models.fields.related_descriptors import ManyToManyDescriptor
from django.urls import reverse

from docs.forms import ProtocolForm
from docs.models import Protocol, Template
from hardware.models import Hardware
from staff.models import Employee
from tests.common import search_field


class TestProtocol:
    def test_protocol_model(self):
        model_fields = Protocol._meta.fields

        date_field = search_field(model_fields, 'date')
        assert date_field is not None, \
            'Модель Protocol должна содержать поле "date"'
        assert isinstance(date_field, DateField), \
            'Поле "date" модели Protocol должно быть DateField'
        assert not date_field.blank, \
            'Поле "date" модели Protocol должно быть обязательным'

        hardware_field = search_field(model_fields, 'hardware_id')
        assert hardware_field is not None, \
            'Модель Protocol должна содержать поле "hardware"'
        assert isinstance(hardware_field, ForeignKey), \
            'Поле "hardware" модели Protocol должно быть ForeignKey'
        assert hardware_field.related_model == Hardware, \
            'Поле hardware модели Protocol должно быть ссылкой на модель Hardware'
        assert not hardware_field.blank, \
            'Поле "hardware" модели Protocol должно быть обязательным'

        assert hasattr(Protocol, 'signers'), \
            'Модель Protocol должна содержать поле "signers"'
        assert isinstance(Protocol.signers, ManyToManyDescriptor), \
            'Поле "signers" модели Protocol должно быть ManyToManyField'

        supervisor_field = search_field(model_fields, 'supervisor_id')
        assert supervisor_field is not None, \
            'Модель Protocol должна содержать поле "supervisor"'
        assert isinstance(supervisor_field, ForeignKey), \
            'Поле "supervisor" модели Protocol должно быть ForeignKey'
        assert supervisor_field.related_model == Employee, \
            'Поле supervisor модели Protocol должно быть ссылкой на модель Employee'
        assert not supervisor_field.blank, \
            'Поле "supervisor" модели Protocol должно быть обязательным'

        assert hasattr(Protocol, 'instruments'), \
            'Модель Protocol должна содержать поле "instruments"'
        assert isinstance(Protocol.instruments, ManyToManyDescriptor), \
            'Поле "instruments" модели Protocol должно быть ManyToManyField'

        template_field = search_field(model_fields, 'template_id')
        assert template_field is not None, \
            'Модель Protocol должна содержать поле "template"'
        assert isinstance(template_field, ForeignKey), \
            'Поле "template" модели Protocol должно быть ForeignKey'
        assert template_field.related_model == Template, \
            'Поле template модели Protocol должно быть ссылкой на модель Template'
        assert not template_field.blank, \
            'Поле "template" модели Protocol должно быть обязательным'

    @pytest.mark.django_db
    def test_protocol_list_view(self, client):
        response = client.get(reverse('docs:protocol-list'))

        assert response.status_code == 200
        assert response.templates[0].name == 'docs/protocol_list.html', \
            'Проверьте, что используете шаблон protocol_list.html в ответе'
        assert 'protocol_list' in response.context, \
            'Проверьте, что передали поле "protocol_list" в контекст страницы'

    @pytest.mark.django_db
    def test_protocol_detail_view(self, client, protocol):
        url = reverse('docs:protocol-detail', kwargs={'pk': protocol.pk})
        response = client.get(url)

        assert response.status_code == 200
        assert 'protocol' in response.context, \
            'Проверьте, что передали поле "protocol" в контекст страницы'

    @pytest.mark.django_db
    def test_protocol_create_view(
        self, auto_login_user, hardware, template, instrument
    ):
        client, user = auto_login_user()
        url = reverse('docs:protocol-create')
        response = client.get(url)

        assert response.status_code == 200
        assert response.context.get('form'), \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], ProtocolForm), \
            'Проверьте, что поле `form` типа ProtocolForm'
        assert response.templates[0].name == 'docs/protocol_form.html', \
            'Проверьте, что используете шаблон protocol_form.html в ответе'

        data = {
            'date': '2000-01-01',
            'template': template.pk,
            'hardware': hardware.pk,
            'signers': [user.pk],
            'supervisor': user.pk,
            'instrument': [instrument.pk],
        }

        response = client.post(url, data=data, follow=True)

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_protocol_update_view_unautorized_user(self, client, protocol):
        url = reverse('docs:protocol-update', kwargs={'pk': protocol.pk})
        response = client.get(url)

        assert (response.status_code in (301, 302)
                and response.url.startswith(reverse('login'))), \
            'Проверьте, что вы переадресуете пользователя на страницу авторизации'

    @pytest.mark.django_db
    def test_protocol_update_view_autorized_user(self, user_client, protocol):
        url = reverse('docs:protocol-update', kwargs={'pk': protocol.pk})
        response = user_client.get(url)

        assert response.status_code == 200
        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], ProtocolForm), \
            'Проверьте, что передали поле `form` типа TemplateForm в контекст страницы'

        data = {
            'date': '2010-12-31',
        }

        response = user_client.post(url, follow=True, data=data)

        assert response.status_code == 200
        assert 'protocol' in response.context, \
            'Проверьте, что передали поле `protocol` в контекст страницы'
        assert isinstance(response.context['protocol'], Protocol), \
            'Проверьте, что поле `protocol` содержит экземпляр `Protocol`'
        assert data['date'] == response.context['protocol'].date.isoformat(), \
            'Проверьте, что экземпляр `Protocol` был изменен'

    @pytest.mark.django_db
    def test_protocol_delete_view_unautorized_user(self, client, protocol):
        url = reverse('docs:protocol-delete', kwargs={'pk': protocol.pk})
        response = client.post(url)

        assert (response.status_code in (301, 302)
                and response.url.startswith(reverse('login'))), \
            'Проверьте, что вы переадресуете пользователя на страницу авторизации'

    @pytest.mark.django_db
    def test_protocol_delete_view_autorized_user(self, user_client, protocol):
        url = reverse('docs:protocol-delete', kwargs={'pk': protocol.pk})
        response = user_client.post(url, follow=True)

        assert response.status_code == 200
        assert response.templates[0].name == 'docs/protocol_list.html', \
            'Проверьте, что используете шаблон protocol_list.html в ответе'
