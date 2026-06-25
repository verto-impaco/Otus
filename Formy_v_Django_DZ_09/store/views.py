from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Product


def product_list(request):
    products = Product.objects.select_related("category")
    return render(request, "store/product_list.html", {"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
    return render(request, "store/product_detail.html", {"product": product})


def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Товар успешно добавлен.")
            return redirect("store:product_detail", pk=product.pk)
    else:
        form = ProductForm()

    return render(
        request,
        "store/product_form.html",
        {"form": form, "title": "Добавить товар", "button_text": "Добавить"},
    )


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Товар успешно обновлен.")
            return redirect("store:product_detail", pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "store/product_form.html",
        {"form": form, "title": "Редактировать товар", "button_text": "Сохранить"},
    )
