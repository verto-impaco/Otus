from models import async_engine, Base


async def create_tables():
    """Создает таблицы в базе данных."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# async def save_users(users_data: Dict[str, Any]):
#     async with AsyncSessionLocal() as session:
#         async with session.begin():
#             data_users = users_data
#             session.add(data_users)


# async def save_posts(posts_data: Dict[str, Any]):
#     async with AsyncSessionLocal() as session:
#         async with session.begin():
#             data_posts = posts_data
#             session.add(data_posts)
