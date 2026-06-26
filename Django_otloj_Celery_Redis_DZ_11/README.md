Интернет-магазин на Django

Небольшой учебный интернет-магазин на Django.

Запуск

1. Создать и активировать виртуальное окружение:

python -m venv .venv
.\.venv\Scripts\Activate.ps1


2. Установить зависимости:

pip install -r requirements.txt


3. Запустить PostgreSQL и Redis через Docker:

docker compose up -d postgres redis


4. Применить миграции:

python manage.py migrate


5. При желании заполнить базу тестовыми товарами:

python manage.py seed_store --clear --categories 5 --products 30 --seed 42


6. Создать администратора:

python manage.py createsuperuser


7. В отдельном терминале запустить Celery worker:

celery -A config worker -l info -P solo


8. Запустить сервер:

python manage.py runserver


Список товаров: http://127.0.0.1:8000/

Добавление товара: http://127.0.0.1:8000/products/add/

Админка: http://127.0.0.1:8000/admin/

Проверка

python -m pytest
python manage.py check


Celery и Redis

Redis используется как брокер Celery:

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0


При добавлении нового товара через страницу /products/add/ приложение ставит
в очередь задачу store.tasks.log_product_created. Worker выводит в консоль
сообщение с названием и ID нового товара.

PostgreSQL

Настройки подключения по умолчанию:

POSTGRES_DB=store_db
POSTGRES_USER=store_user
POSTGRES_PASSWORD=store_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5433


Такие же значения указаны в docker-compose.yml
