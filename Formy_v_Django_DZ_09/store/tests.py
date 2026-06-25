from decimal import Decimal

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .forms import ProductForm
from .models import Category, Product


class SeedStoreCommandTests(TestCase):
    def test_seed_store_creates_requested_objects(self):
        call_command("seed_store", categories=2, products=5, seed=1)

        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Product.objects.count(), 5)
        self.assertTrue(Product.objects.filter(category__isnull=False).exists())


class ProductFormTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Электроника")

    def test_form_validates_positive_price(self):
        form = ProductForm(
            data={
                "category": self.category.pk,
                "name": "Клавиатура",
                "description": "Механическая клавиатура.",
                "price": "0",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("price", form.errors)

    def test_form_saves_valid_product(self):
        form = ProductForm(
            data={
                "category": self.category.pk,
                "name": "Клавиатура",
                "description": "Механическая клавиатура.",
                "price": "2999.90",
            }
        )

        self.assertTrue(form.is_valid())
        product = form.save()
        self.assertEqual(product.price, Decimal("2999.90"))


class ProductViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Книги")
        self.product = Product.objects.create(
            category=self.category,
            name="Книга по Django",
            description="Учебное пособие.",
            price=Decimal("1500.00"),
        )

    def test_product_list_page_displays_products(self):
        response = self.client.get(reverse("store:product_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.description)
        self.assertContains(response, "1500,00")

    def test_product_detail_page_displays_full_product_data(self):
        response = self.client.get(
            reverse("store:product_detail", kwargs={"pk": self.product.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.category.name)
        self.assertContains(response, self.product.description)
        self.assertContains(response, "1500,00")

    def test_product_create_view_creates_product(self):
        response = self.client.post(
            reverse("store:product_create"),
            data={
                "category": self.category.pk,
                "name": "Новая книга",
                "description": "Описание новой книги.",
                "price": "900.00",
            },
        )

        product = Product.objects.get(name="Новая книга")
        self.assertRedirects(
            response, reverse("store:product_detail", kwargs={"pk": product.pk})
        )
        self.assertEqual(product.price, Decimal("900.00"))

    def test_product_update_view_updates_product(self):
        response = self.client.post(
            reverse("store:product_update", kwargs={"pk": self.product.pk}),
            data={
                "category": self.category.pk,
                "name": "Книга по Django 6",
                "description": "Обновленное описание.",
                "price": "1800.00",
            },
        )

        self.product.refresh_from_db()
        self.assertRedirects(
            response,
            reverse("store:product_detail", kwargs={"pk": self.product.pk}),
        )
        self.assertEqual(self.product.name, "Книга по Django 6")
        self.assertEqual(self.product.price, Decimal("1800.00"))
