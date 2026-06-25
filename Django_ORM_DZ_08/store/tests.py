from django.core.management import call_command
from django.test import TestCase

from .models import Category, Product


class SeedStoreCommandTests(TestCase):
    def test_seed_store_creates_requested_objects(self):
        call_command("seed_store", categories=2, products=5, seed=1)

        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Product.objects.count(), 5)
        self.assertTrue(Product.objects.filter(category__isnull=False).exists())
