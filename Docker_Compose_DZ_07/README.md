# Docker Compose homework

Flask-приложение с PostgreSQL в отдельном контейнере.

Запуск:

```bash
docker compose up --build
```

Приложение будет доступно на `http://localhost:8080`.

Страницы:

- `/users` - список пользователей
- `/users/new` - добавить пользователя
- `/posts` - список записей
- `/posts/new` - добавить запись

В compose используются три сервиса: `db`, `web`, `nginx`.
