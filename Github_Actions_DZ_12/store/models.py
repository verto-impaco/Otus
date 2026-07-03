from django.db import models


class Category(models.Model):
    name = models.CharField("название", max_length=120, unique=True)
    description = models.TextField("описание", blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="категория",
    )
    name = models.CharField("название", max_length=160)
    description = models.TextField("описание", blank=True)
    price = models.DecimalField("цена", max_digits=10, decimal_places=2)
    created_at = models.DateTimeField("дата создания", auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "name"]
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name
