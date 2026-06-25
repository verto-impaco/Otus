# Магазин на Django

Небольшой проект для домашнего задания по шаблонам и формам в Django.

В проекте есть приложение `store`, две модели (`Category` и `Product`),
страницы списка и деталей товаров, формы добавления и редактирования,
настройка админки и команда для заполнения базы тестовыми данными.
База данных используется только PostgreSQL.

## Запуск

1. Создать и активировать виртуальное окружение:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Установить зависимости:

```powershell
pip install -r requirements.txt
```

3. Запустить PostgreSQL через Docker:

```powershell
docker compose up -d postgres
```

4. Применить миграции:

```powershell
python manage.py migrate
```

5. Заполнить базу:

```powershell
python manage.py seed_store --clear --categories 5 --products 30 --seed 42
```

6. Создать администратора:

```powershell
python manage.py createsuperuser
```

7. Запустить сервер:

```powershell
python manage.py runserver
```

Список товаров: http://127.0.0.1:8000/

Добавление товара: http://127.0.0.1:8000/products/add/

Админка: http://127.0.0.1:8000/admin/

## Что реализовано

- Базовый шаблон `base.html` с `block` и наследованием через `extends`.
- Страница списка товаров с названием, описанием и ценой.
- Страница деталей товара со всеми данными.
- Форма добавления нового товара.
- Форма редактирования товара.
- Отображение ошибок валидации в шаблоне формы.
- Админка с `list_display`, `list_filter`, `search_fields`.
- Кастомные действия админки для снижения и повышения цены выбранных товаров.

## PostgreSQL

Настройки подключения по умолчанию:

```text
POSTGRES_DB=store_db
POSTGRES_USER=store_user
POSTGRES_PASSWORD=store_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
```

Такие же значения указаны в `docker-compose.yml`.
