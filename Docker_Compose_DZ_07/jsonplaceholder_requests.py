"""
создайте асинхронные функции для выполнения запросов к ресурсам (используйте aiohttp)
"""
from typing import Any
import logging
import aiohttp
from models import User, Post

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


async def fetch_json(
        url: str,
) -> dict[str, Any]:
    logging.info(f"Fetching data from {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.json()

    logging.info(f"Got data from {url}: {result}")
    return result


async def fetch_users_data():
    users_result = await fetch_json(USERS_DATA_URL)
    users = []

    for that_user in users_result:
        user = User(
            id=that_user.get('id'),
            name=that_user.get('name'),
            username=that_user.get('username'),
            email=that_user.get('email')
        )
        users.append(user)
    return users


async def fetch_posts_data():
    posts_result = await fetch_json(POSTS_DATA_URL)
    posts = []

    for that_post in posts_result:
        post = Post(
            id= that_post.get('id'),
            userId = that_post.get('userId'),
            title = that_post.get('title'),
            body = that_post.get('body')
        )
        posts.append(post)
    return posts
