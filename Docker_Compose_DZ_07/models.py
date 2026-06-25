"""
* создайте алхимичный engine
* добавьте declarative base (свяжите с engine)
создайте объект Session
* добавьте модели User и Post, объявите поля:
* для модели User обязательными являются name, username, email
* для модели Post обязательными являются user_id, title, body
* создайте связи relationship между моделями: User.posts и Post.user
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


class Base(DeclarativeBase):
    pass


PG_CONN_URI = os.environ.get(
    "SQLALCHEMY_PG_CONN_URI") or "postgresql+asyncpg://postgres:password@localhost/postgres"


async_engine = create_async_engine(PG_CONN_URI)


AsyncSessionLocal = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False,)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column('user_id', Integer, ForeignKey(
        'users.id'), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)

    user = relationship("User", back_populates="posts")
