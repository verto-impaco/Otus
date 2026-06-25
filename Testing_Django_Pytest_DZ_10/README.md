# Интернет-магазин на Django

Учебный проект по class-based views и тестам на pytest.

В приложении `store` есть категории и товары. Для товаров сделаны страницы
списка, просмотра, добавления, редактирования и удаления. Для проверки работы
моделей, форм и views написаны автотесты.

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

5. При желании заполнить базу тестовыми товарами:

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

## Проверка

```powershell
python -m pytest
python manage.py check
```

Для pytest используется отдельная тестовая настройка с SQLite, поэтому
PostgreSQL не нужен для запуска тестов.

## Что сделано

- `ListView` для списка товаров.
- `DetailView` для страницы товара.
- `CreateView` и `UpdateView` для формы товара.
- `DeleteView` для удаления товара.
- Pytest-тесты для CRUD-операций модели.
- Тесты формы и основных страниц.

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
