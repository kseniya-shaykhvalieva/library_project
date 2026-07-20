# API для управления библиотекой

Веб-приложение на Django для управления библиотекой: книги, авторы, выдачи, пользователи.

## Основной функционал

- CRUD для книг, авторов, выдач.
- Авторизация через JWT.
- Разграничение прав: админ управляет всем, пользователь — только своим профилем.
- Поиск, фильтрация, сортировка и пагинация для книг.
- Валидация:
  - Количество доступных экземпляров не может превышать общее.
  - Дата возврата не может быть раньше даты выдачи.
  - Книга не может дублироваться (название + автор).
  - Нельзя удалить пользователя с активными выдачами.
- Автоматическое изменение количества доступных экземпляров при выдаче/возврате.
- API-документация (Swagger/ReDoc).
- Покрытие тестами ≥75%.
- Контейнеризация (Docker, Docker Compose).
- CI/CD (GitHub Actions).

## Структура проекта
``` 
library_project/
├── .github/
│   └── workflows/
│       └── ci.yml
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── htmlcov/
├── library/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── paginations.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── validations.py
│   └── views.py
├── media/
├── staticfiles/
├── users/
│   ├── management/commands/
│   │   ├── __init__.py
│   │   └── csu.py
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── .coverage
├── .dockerignore
├── .env
├── .env_template
├── .flake8
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── nginx.conf
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Установка и запуск (локально)

1. Клонирование и переход в директорию

2. Установка зависимостей через Poetry:

``` 
poetry install
```

3. Настройка переменных окружения:
- Скопируйте `.env_template` в `.env`
- Заполните параметры базы данных и секретный ключ

4. Применение миграций и создание суперпользователя:
``` 
python manage.py migrate
python manage.py csu
```
5. Запуск сервера:
``` 
python manage.py runserver
```
## Запуск через Docker

1. Сборка и запуск контейнеров:
``` 
docker-compose up --build
```
2. Применение миграций в контейнере:
``` 
docker-compose exec web python manage.py migrate
```
3. Создание суперпользователя:
``` 
docker-compose exec web python manage.py csu
```
4. Остановка контейнеров:
``` 
docker-compose down
```

## API эндпоинты

- `POST /users/register/` — регистрация пользователя
- `POST /users/login/` — получение JWT-токена
- `GET /library/authors/` — список авторов
- `POST /library/authors/` — создание автора (админ)
- `GET /library/books/` — список книг (поиск, фильтрация, пагинация)
- `POST /library/books/` — создание книги (админ)
- `GET /library/loans/` — список выдач
- `POST /library/loans/` — создание выдачи (админ)
- `PATCH /library/loans/<id>/` — возврат книги (админ)

Подробнее: `/api/docs/` (Swagger) и `/api/redoc/` (ReDoc).

## Инструменты

- Python 3.14
- Django 6.0.7
- Django REST Framework 3.17.1
- djangorestframework-simplejwt 5.5.1
- django-filter 26.1
- drf-spectacular 0.30.0
- django-cors-headers 4.9.0
- PostgreSQL (psycopg2-binary 2.9.12)
- Nginx
- Docker + Docker Compose
- GitHub Actions
- Poetry
- coverage 7.15.2
- flake8, mypy, isort, black
