import random

import factory.random
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from store.factories import CategoryFactory, ProductFactory
from store.models import Category, Product


class Command(BaseCommand):
    help = "Создает примерные категории и товары через фабрики."

    def add_arguments(self, parser):
        parser.add_argument(
            "--categories",
            type=int,
            default=5,
            help="Сколько категорий создать.",
        )
        parser.add_argument(
            "--products",
            type=int,
            default=30,
            help="Сколько товаров создать.",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Удалить старые товары и категории перед заполнением.",
        )
        parser.add_argument(
            "--seed",
            type=int,
            help="Зерно генератора для повторяемых данных.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        categories_count = options["categories"]
        products_count = options["products"]
        seed = options["seed"]

        if categories_count < 1:
            raise CommandError("--categories должно быть больше 0.")
        if products_count < 0:
            raise CommandError("--products не может быть отрицательным.")

        if seed is not None:
            random.seed(seed)
            factory.random.reseed_random(seed)

        if options["clear"]:
            Product.objects.all().delete()
            Category.objects.all().delete()

        categories = CategoryFactory.create_batch(categories_count)
        products = [
            ProductFactory(category=random.choice(categories))
            for _ in range(products_count)
        ]

        self.stdout.write(
            self.style.SUCCESS(
                f"Создано категорий: {len(categories)}, товаров: {len(products)}."
            )
        )
