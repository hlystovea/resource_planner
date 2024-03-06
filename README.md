# Resource planner

![Static Badge](https://img.shields.io/badge/hlystovea-resource_planner-resource_planner)
![GitHub top language](https://img.shields.io/github/languages/top/hlystovea/resource_planner)
![GitHub](https://img.shields.io/github/license/hlystovea/resource_planner)
![GitHub Repo stars](https://img.shields.io/github/stars/hlystovea/resource_planner)
![GitHub issues](https://img.shields.io/github/issues/hlystovea/resource_planner)
![workflow badge](https://github.com/hlystovea/resource_planner/actions/workflows/main.yml/badge.svg)

## Описание
Сервис предназначен для учета и планирования использования ресурсов предприятия.

## Возможности
На данный момент поддерживается следующий функционал:
- Учет хранения материалов и инструмента
- Учет дефектов оборудования
- Планирование ремонтов и подсчет трудозатрат в чел./ч (только админка)
- Учет персонала и подсчет его численности по подразделениям (только админка)

## Технологии
- Python 3.9
- Django 4.2
- Docker
- Nginx
- Postgres

## Установка (Linux)
У вас должен быть установлен [Docker Compose](https://docs.docker.com/compose/)

1. Клонирование репозитория

```git clone https://github.com/hlystovea/resource_planner.git```  

2. Переход в директорию resource_planner

```cd resource_planner```

3. Создание файла с переменными окружения

```cp env.example .env```

4. Заполнение файла .env своими переменными

```nano .env```

5. Запуск проекта

```sudo docker compose up -d```

6. Запуск миграций

```sudo docker compose exec backend python manage.py migrate --noinput```

7. Сбор статических файлов

```sudo docker compose exec backend python manage.py collectstatic --no-input```

8. Создание суперпользователя

```sudo docker compose exec backend python manage.py createsuperuser```

9. Сайт будет доступен по адресу
 
```http://127.0.0.1:8001```

10. Админка сайта будет доступна по адресу

```http://127.0.0.1:8001/admin```


