from decimal import Decimal
from random import randint

import factory

from .models import Category, Product


CATEGORY_NAMES = [
    "Электроника",
    "Книги",
    "Одежда",
    "Дом и кухня",
    "Спорт",
]

CATEGORY_DESCRIPTIONS = [
    "Товары для дома, учебы и повседневных задач.",
    "Подборка популярных товаров с описанием и ценами.",
    "Категория для демонстрации работы связей в ORM.",
]

PRODUCT_NAMES = [
    "Беспроводная мышь",
    "Настольная лампа",
    "Рюкзак городской",
    "Термокружка",
    "Ежедневник",
    "Клавиатура",
    "Футболка",
    "Книга по Python",
    "Коврик для йоги",
    "Органайзер",
]

PRODUCT_DESCRIPTIONS = [
    "Обычный товар для проверки списка и карточки в админке.",
    "Добавлен через фабрику, чтобы быстро заполнить базу тестовыми данными.",
    "Подходит для демонстрации фильтрации, поиска и сортировки.",
]


def category_name(number):
    if number < len(CATEGORY_NAMES):
        return CATEGORY_NAMES[number]
    return f"Категория {number + 1}"


def product_name(number):
    name = PRODUCT_NAMES[number % len(PRODUCT_NAMES)]
    return f"{name} {number + 1}"


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)

    name = factory.Sequence(category_name)
    description = factory.Iterator(CATEGORY_DESCRIPTIONS)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    name = factory.Sequence(product_name)
    description = factory.Iterator(PRODUCT_DESCRIPTIONS)
    price = factory.LazyFunction(lambda: Decimal(randint(100, 100000)) / Decimal("100"))
