import pytest


class TestErrors:
    @pytest.mark.django_db
    def test_bad_request_view(self, client):
        try:
            response = client.get('/400/')
        except Exception as e:
            assert False, f'Тест работает не правильно. Ошибка: {e}'

        assert response.status_code == 400
        assert response.templates[0].name == 'errors/400.html', \
            'Проверьте, что используете шаблон 400.html в ответе'

    @pytest.mark.django_db
    def test_permission_denied_view(self, client):
        try:
            response = client.get('/403/')
        except Exception as e:
            assert False, f'Тест работает не правильно. Ошибка: {e}'

        assert response.status_code == 403
        assert response.templates[0].name == 'errors/403.html', \
            'Проверьте, что используете шаблон 403.html в ответе'

    @pytest.mark.django_db
    def test_not_found_view(self, client):
        try:
            response = client.get('/404/')
        except Exception as e:
            assert False, f'Тест работает не правильно. Ошибка: {e}'

        assert response.status_code == 404
        assert response.templates[0].name == 'errors/404.html', \
            'Проверьте, что используете шаблон 404.html в ответе'
