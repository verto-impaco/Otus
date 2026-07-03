from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ProductForm
from .models import Product
from .tasks import log_product_created


class ProductListView(ListView):
    model = Product
    template_name = "store/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.select_related("category")


class ProductDetailView(DetailView):
    model = Product
    template_name = "store/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.select_related("category")


class ProductCreateView(SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "store/product_form.html"
    success_message = "Товар успешно добавлен."
    extra_context = {
        "title": "Добавить товар",
        "button_text": "Добавить",
    }

    def form_valid(self, form):
        response = super().form_valid(form)
        transaction.on_commit(
            lambda: log_product_created.delay(self.object.pk, self.object.name)
        )
        return response

    def get_success_url(self):
        return reverse("store:product_detail", kwargs={"pk": self.object.pk})


class ProductUpdateView(SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "store/product_form.html"
    context_object_name = "product"
    success_message = "Товар успешно обновлен."
    extra_context = {
        "title": "Редактировать товар",
        "button_text": "Сохранить",
    }

    def get_queryset(self):
        return Product.objects.select_related("category")

    def get_success_url(self):
        return reverse("store:product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "store/product_confirm_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("store:product_list")

    def get_queryset(self):
        return Product.objects.select_related("category")

    def form_valid(self, form):
        messages.success(self.request, "Товар успешно удален.")
        return super().form_valid(form)
