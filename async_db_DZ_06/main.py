"""
Домашнее задание №4
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""
import asyncio
from db import create_tables
from jsonplaceholder_requests import fetch_users_data, fetch_posts_data
from models import AsyncSessionLocal
import logging
from sqlalchemy import text


async def async_main():
    await create_tables()
    try:
        save_users, save_posts = await asyncio.gather(
            fetch_users_data(),
            fetch_posts_data()
        )

        if not save_users or not save_posts:
            raise ValueError("No data to save")

        async with AsyncSessionLocal() as session:
            await session.execute(text("TRUNCATE TABLE posts RESTART IDENTITY CASCADE"))
            await session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
            await session.commit()

            async with session.begin():
                session.add_all(save_users)

        async with AsyncSessionLocal() as session:
            async with session.begin():
                session.add_all(save_posts)


    except Exception as e:
        logging.error(f'Failed {e}')
        raise


def main():
    return asyncio.run(async_main())


if __name__ == "__main__":
    main()
