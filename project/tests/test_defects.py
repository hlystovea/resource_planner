import pytest

from django import forms
from django.db.models import fields
from django.urls import reverse
from django_resized import ResizedImageField
from sorl.thumbnail.fields import ImageFormField

from defects.forms import DefectForm
from defects.models import Defect
from staff.models import Employee


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


def get_field_context(context, field_type):
    for field in context.keys():
        if field not in ('user', 'request') and type(context[field]) == field_type:
            return context[field]


class TestDefect:

    def test_defect_model(self):
        model_fields = Defect._meta.fields

        date_field = search_field(model_fields, 'date')
        assert date_field is not None, 'Модель Defect должна содержать поле "date"'
        assert type(date_field) == fields.DateField, \
            'Поле "date" модели Defect должно быть DateField'
        assert not date_field.blank, \
            'Поле "date" модели Defect должно быть обязательным'

        part_field = search_field(model_fields, 'part_id')
        assert part_field is not None, \
            'Модель Defect должна содержать поле "part"'
        assert type(part_field) == fields.related.ForeignKey, \
            'Поле "part" модели Defect должно быть ForeignKey'
        assert not part_field.blank, \
            'Поле "part" модели Defect должно быть обязательным'

        employee_field = search_field(model_fields, 'employee_id')
        assert employee_field is not None, \
            'Модель Defect должна содержать поле "employee"'
        assert type(employee_field) == fields.related.ForeignKey, \
            'Поле "employee" модели Defect должно быть ForeignKey'
        assert employee_field.related_model == Employee, \
            'Поле employee модели Defect должно быть ссылкой на модель Employee'
        assert not employee_field.blank, \
            'Поле "employee" модели Defect должно быть обязательным'

        description_field = search_field(model_fields, 'description')
        assert description_field is not None, \
            'Модель Defect должна содержать поле "description"'
        assert type(description_field) == fields.TextField, \
            'Поле description модели Defect должно быть текстовым TextField'
        assert not description_field.blank, \
            'Поле description модели Defect должно быть обязательным'

        image_field = search_field(model_fields, 'image')
        assert image_field is not None, \
            'Модель Defect должна содержать поле "image"'
        assert type(image_field) == ResizedImageField, \
            'Поле "image" модели Defect должно быть ResizedImageField'
        assert image_field.blank, \
            'Поле "image" модели Defect не должно быть обязательным'

        attachment_field = search_field(model_fields, 'attachment')
        assert attachment_field is not None, \
            'Модель Defect должна содержать поле "attachment"'
        assert type(attachment_field) == fields.files.FileField, \
            'Поле "attachment" модели Defect должно быть FileField'
        assert attachment_field.blank, \
            'Поле "attachment" модели Defect не должно быть обязательным'

        repair_method_field = search_field(model_fields, 'repair_method_id')
        assert repair_method_field is not None, \
            'Модель Defects должна содержать поле repair_method'
        assert type(repair_method_field) == fields.related.ForeignKey, \
            'Поле repair_method должно быть ForeignKey'
        assert repair_method_field.blank, \
            'Поле repair_method не должно быть обязательным'

    @pytest.mark.django_db
    def test_defect_view_get_list(self, client):
        try:
            url = reverse('defects:defect-list')
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'

        assert response.status_code == 200
        assert 'defect_list' in response.context, \
            'Проверьте, что передали поле "defect_list" в контекст страницы'

    @pytest.mark.django_db
    def test_defect_view_get_detail(self, client, defect):
        try:
            url = reverse(
                'defects:defect-detail', kwargs={'pk': defect.id}
            )
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'

        assert response.status_code == 200
        assert type(response.context.get('defect')) == Defect, \
            'Проверьте, что передали поле типа Defect в контекст страницы'

    @pytest.mark.django_db
    def test_defect_view_create(self, user_client):
        try:
            url = reverse('defects:defect-create')
            response = user_client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'

        assert response.status_code != 404, \
            'Страница не найдена, проверьте этот адрес в *urls.py*'

        form = get_field_context(response.context, DefectForm)
        assert form, \
            'Проверьте, что передали поле `form` типа DefectForm в контекст стр.'

    @pytest.mark.django_db
    def test_defect_view_update_unautorized_user(self, client, defect):
        try:
            url = reverse('defects:defect-update', kwargs={'pk': defect.id})
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'

        assert response.status_code != 404, \
            'Страница не найдена, проверьте этот адрес в *urls.py*'

        assert response.status_code in (301, 302) and response.url.startswith(reverse('login')), \
            'Проверьте, что вы переадресуете пользователя на страницу авторизации'


    @pytest.mark.django_db
    def test_defect_view_update_autorized_user(self, user_client, defect):
        try:
            url = reverse('defects:defect-update', kwargs={'pk': defect.id})
            response = user_client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'

        assert response.status_code != 404, \
            'Страница не найдена, проверьте этот адрес в *urls.py*'

        assert response.status_code == 200
        assert type(response.context.get('form')) == DefectForm, \
            'Проверьте, что передали поле `form` типа DefectForm в контекст страницы'

        defect_context = get_field_context(response.context, Defect)
        assert defect_context is not None, \
            'Проверьте, что передали дефект в контекст страницы'
        

    @pytest.mark.django_db
    def test_defect_view_delete_unautorized_user(self, client, defect):
        try:
            url = reverse('defects:defect-delete', kwargs={'pk': defect.id})
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'

        assert response.status_code != 404, \
            'Страница не найдена, проверьте этот адрес в *urls.py*'

        assert response.status_code in (301, 302) and response.url.startswith(reverse('login')), \
            'Проверьте, что вы переадресуете пользователя на страницу авторизации'

    @pytest.mark.django_db
    def test_defect_view_delete_autorized_user(self, user_client, defect):
        try:
            url = reverse('defects:defect-delete', kwargs={'pk': defect.id})
            response = user_client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'

        assert response.status_code != 404, \
            'Страница не найдена, проверьте этот адрес в *urls.py*'
