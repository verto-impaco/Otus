from decimal import Decimal

import pytest
from django.core.management import call_command
from django.urls import reverse

from .forms import ProductForm
from .models import Category, Product


pytestmark = pytest.mark.django_db


@pytest.fixture
def category():
    return Category.objects.create(name="Книги")


@pytest.fixture
def product(category):
    return Product.objects.create(
        category=category,
        name="Книга по Django",
        description="Учебное пособие.",
        price=Decimal("1500.00"),
    )


def test_seed_store_creates_requested_objects():
    call_command("seed_store", categories=2, products=5, seed=1)

    assert Category.objects.count() == 2
    assert Product.objects.count() == 5
    assert Product.objects.filter(category__isnull=False).exists()


def test_product_model_create(category):
    product = Product.objects.create(
        category=category,
        name="Новый товар",
        description="Описание нового товара.",
        price=Decimal("999.90"),
    )

    created_product = Product.objects.get(pk=product.pk)
    assert created_product.name == "Новый товар"
    assert created_product.description == "Описание нового товара."
    assert created_product.price == Decimal("999.90")
    assert created_product.category == category
    assert str(created_product) == "Новый товар"


def test_product_model_read(product):
    found_product = Product.objects.get(pk=product.pk)

    assert found_product.name == "Книга по Django"
    assert found_product.category.name == "Книги"
    assert found_product.description == "Учебное пособие."
    assert found_product.price == Decimal("1500.00")


def test_product_model_update(product):
    product.name = "Книга по Django 6"
    product.price = Decimal("1800.00")
    product.save(update_fields=["name", "price"])

    product.refresh_from_db()
    assert product.name == "Книга по Django 6"
    assert product.price == Decimal("1800.00")


def test_product_model_delete(product):
    product_pk = product.pk

    product.delete()

    assert not Product.objects.filter(pk=product_pk).exists()


def test_form_validates_positive_price(category):
    form = ProductForm(
        data={
            "category": category.pk,
            "name": "Клавиатура",
            "description": "Механическая клавиатура.",
            "price": "0",
        }
    )

    assert not form.is_valid()
    assert "price" in form.errors


def test_form_saves_valid_product(category):
    form = ProductForm(
        data={
            "category": category.pk,
            "name": "Клавиатура",
            "description": "Механическая клавиатура.",
            "price": "2999.90",
        }
    )

    assert form.is_valid()
    product = form.save()
    assert product.price == Decimal("2999.90")


def test_product_list_page_displays_products(client, product):
    response = client.get(reverse("store:product_list"))
    content = response.content.decode()

    assert response.status_code == 200
    assert product.name in content
    assert product.description in content
    assert "1500,00" in content


def test_product_detail_page_displays_full_product_data(client, product):
    response = client.get(reverse("store:product_detail", kwargs={"pk": product.pk}))
    content = response.content.decode()

    assert response.status_code == 200
    assert product.name in content
    assert product.category.name in content
    assert product.description in content
    assert "1500,00" in content


def test_product_create_view_creates_product(client, category):
    response = client.post(
        reverse("store:product_create"),
        data={
            "category": category.pk,
            "name": "Новая книга",
            "description": "Описание новой книги.",
            "price": "900.00",
        },
    )

    product = Product.objects.get(name="Новая книга")
    assert response.status_code == 302
    assert response.url == reverse("store:product_detail", kwargs={"pk": product.pk})
    assert product.price == Decimal("900.00")


def test_product_update_view_updates_product(client, product):
    response = client.post(
        reverse("store:product_update", kwargs={"pk": product.pk}),
        data={
            "category": product.category.pk,
            "name": "Книга по Django 6",
            "description": "Обновленное описание.",
            "price": "1800.00",
        },
    )

    product.refresh_from_db()
    assert response.status_code == 302
    assert response.url == reverse("store:product_detail", kwargs={"pk": product.pk})
    assert product.name == "Книга по Django 6"
    assert product.price == Decimal("1800.00")


def test_product_delete_confirmation_page_displays_product(client, product):
    response = client.get(reverse("store:product_delete", kwargs={"pk": product.pk}))
    content = response.content.decode()

    assert response.status_code == 200
    assert "Удалить товар" in content
    assert product.name in content


def test_product_delete_view_deletes_product(client, product):
    product_pk = product.pk

    response = client.post(reverse("store:product_delete", kwargs={"pk": product_pk}))

    assert response.status_code == 302
    assert response.url == reverse("store:product_list")
    assert not Product.objects.filter(pk=product_pk).exists()
