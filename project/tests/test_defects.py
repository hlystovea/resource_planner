import pytest

from django.db.models.fields import DateField, TextField
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.files import FileField
from django.urls import reverse
from django_resized import ResizedImageField

from defects.forms import DefectForm
from defects.models import Defect
from staff.models import Employee
from tests.common import search_field, get_field_context


class TestDefect:
    def test_defect_model(self):
        model_fields = Defect._meta.fields

        date_field = search_field(model_fields, 'date')
        assert date_field is not None, 'Модель Defect должна содержать поле "date"'
        assert isinstance(date_field, DateField), \
            'Поле "date" модели Defect должно быть DateField'
        assert not date_field.blank, \
            'Поле "date" модели Defect должно быть обязательным'

        part_field = search_field(model_fields, 'part_id')
        assert part_field is not None, \
            'Модель Defect должна содержать поле "part"'
        assert isinstance(part_field, ForeignKey), \
            'Поле "part" модели Defect должно быть ForeignKey'
        assert not part_field.blank, \
            'Поле "part" модели Defect должно быть обязательным'

        employee_field = search_field(model_fields, 'employee_id')
        assert employee_field is not None, \
            'Модель Defect должна содержать поле "employee"'
        assert isinstance(employee_field, ForeignKey), \
            'Поле "employee" модели Defect должно быть ForeignKey'
        assert employee_field.related_model == Employee, \
            'Поле employee модели Defect должно быть ссылкой на модель Employee'
        assert not employee_field.blank, \
            'Поле "employee" модели Defect должно быть обязательным'

        description_field = search_field(model_fields, 'description')
        assert description_field is not None, \
            'Модель Defect должна содержать поле "description"'
        assert isinstance(description_field, TextField), \
            'Поле description модели Defect должно быть текстовым TextField'
        assert not description_field.blank, \
            'Поле description модели Defect должно быть обязательным'

        image_field = search_field(model_fields, 'image')
        assert image_field is not None, \
            'Модель Defect должна содержать поле "image"'
        assert isinstance(image_field, ResizedImageField), \
            'Поле "image" модели Defect должно быть ResizedImageField'
        assert image_field.blank, \
            'Поле "image" модели Defect не должно быть обязательным'

        attachment_field = search_field(model_fields, 'attachment')
        assert attachment_field is not None, \
            'Модель Defect должна содержать поле "attachment"'
        assert isinstance(attachment_field, FileField), \
            'Поле "attachment" модели Defect должно быть FileField'
        assert attachment_field.blank, \
            'Поле "attachment" модели Defect не должно быть обязательным'

        repair_method_field = search_field(model_fields, 'repair_method_id')
        assert repair_method_field is not None, \
            'Модель Defects должна содержать поле repair_method'
        assert isinstance(repair_method_field, ForeignKey), \
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
        assert 'defect' in response.context, \
            'Проверьте, что передали поле `defect` в контекст страницы'
        assert isinstance(response.context['defect'], Defect), \
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

        assert (response.status_code in (301, 302)
                and response.url.startswith(reverse('login'))), \
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
        assert 'form' in response.context, \
            'Проверьте, что передали поле `form` в контекст страницы'
        assert isinstance(response.context['form'], DefectForm), \
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

        assert (response.status_code in (301, 302)
                and response.url.startswith(reverse('login'))), \
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


class TestStatistics:

    @pytest.mark.django_db
    def test_defect_years_view(self, client, defect):
        try:
            url = reverse('api:defect-years')
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'

        assert response.status_code == 200

        assert 'years' in response.data, \
            'Проверьте, что передали поле `years`.'

    @pytest.mark.django_db
    def test_defect_statistics_by_group_view(self, client):
        try:
            url = reverse('api:defect-statistics-by-group')
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_defect_statistics_by_tech_reason(self, client):
        try:
            url = reverse('api:defect-statistics-by-tech-reason')
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_defect_statistics_by_org_reason(self, client):
        try:
            url = reverse('api:defect-statistics-by-org-reason')
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_defect_statistics_by_repair_method(self, client):
        try:
            url = reverse('api:defect-statistics-by-repair-method')
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_defect_statistics_view(self, client):
        try:
            url = reverse('defects:defect-statistics')
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница работает не правильно. Ошибка: {e}'

        assert response.status_code == 200
