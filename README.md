# Resource planner

### Описание
Сервис предназначен для учета и планирования использования ресурсов предприятия.

### Возможности
На данный момент поддерживается следующий функционал:
- Учет хранения материалов и инструмента
- Планирование ремонтов и подсчет трудозатрат в чел./ч
- Учет персонала и подсчет его численности по подразделениям

### Технологии
- Python 3.9
- Django 3.2.3
- Docker
- Nginx
- Postgres

### Начало работы

1. Склонируйте проект:


```git clone https://github.com/hlystovea/resource_planner.git```  


2. Создайте файл .env по примеру env.example.


3. Запустите контейнеры:

```docker-compose up -d```


4. Запустите миграции:

```docker-compose exec backend python manage.py migrate --noinput```

5. Соберите статику:

```docker-compose exec backend python manage.py collectstatic --no-input```

6. Создайте своего суперпользователя:

```docker-compose exec backend python manage.py createsuperuser```

7. Сайт будет доступен по адресу:
 
```http://127.0.0.1```


