# Магазин на Django

Небольшой каталог товаров на Django.

В приложении `store` есть категории и товары. Для товаров сделаны страницы
списка, просмотра, добавления, редактирования и удаления. При добавлении товара
запускается Celery-задача, которая выводит информацию о товаре в консоль worker.

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

3. Запустить PostgreSQL и Redis через Docker:

```powershell
docker compose up -d postgres redis
```

4. Применить миграции:

```powershell
python manage.py migrate
```

5. При желании заполнить базу примерными товарами:

```powershell
python manage.py seed_store --clear --categories 5 --products 30 --seed 42
```

6. Создать администратора:

```powershell
python manage.py createsuperuser
```

7. В отдельном терминале запустить Celery worker:

```powershell
celery -A config worker -l info -P solo
```

8. Запустить сервер:

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

Для pytest используется отдельная настройка с SQLite, поэтому
PostgreSQL и Redis не нужны для запуска тестов. Celery-задачи в тестах
выполняются синхронно.

## CI

Тесты запускаются в GitHub Actions через workflow
`.github/workflows/tests.yml`. В CI дополнительно собирается отчет покрытия
`coverage.xml`; если в настройках репозитория есть секрет `CODECOV_TOKEN`,
отчет отправляется в Codecov.

## Celery и Redis

Redis используется как брокер Celery:

```text
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

При добавлении нового товара через страницу `/products/add/` приложение ставит
в очередь задачу `store.tasks.log_product_created`. Worker выводит в консоль
сообщение с названием и ID нового товара.

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
