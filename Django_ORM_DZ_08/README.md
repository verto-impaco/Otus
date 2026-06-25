# Магазин на Django

Небольшой проект для домашнего задания по Django ORM.

В проекте есть приложение `store`, две модели (`Category` и `Product`),
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

Админка: http://127.0.0.1:8000/admin/

## PostgreSQL

Настройки подключения по умолчанию:

```text
POSTGRES_DB=store_db
POSTGRES_USER=store_user
POSTGRES_PASSWORD=store_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Такие же значения указаны в `docker-compose.yml`.
