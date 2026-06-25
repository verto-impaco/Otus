from decimal import Decimal

from django.contrib import admin
from django.db.models import Count, F

from .models import Category, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ("name", "price", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (ProductInline,)
    list_display = ("name", "products_count")
    search_fields = ("name", "description")
    ordering = ("name",)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("products"))

    @admin.display(ordering="products_count", description="Товаров")
    def products_count(self, obj):
        return obj.products_count


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ("apply_discount_10", "increase_price_10")
    autocomplete_fields = ("category",)
    date_hierarchy = "created_at"
    fieldsets = (
        (None, {"fields": ("name", "category", "price")}),
        ("Описание", {"fields": ("description", "created_at")}),
    )
    list_display = ("name", "category", "price", "created_at")
    list_filter = ("category", "created_at")
    list_per_page = 25
    list_select_related = ("category",)
    ordering = ("-created_at", "name")
    readonly_fields = ("created_at",)
    search_fields = ("name", "description", "category__name")

    @admin.action(description="Снизить цену выбранных товаров на 10%")
    def apply_discount_10(self, request, queryset):
        updated = queryset.update(price=F("price") * Decimal("0.90"))
        self.message_user(request, f"Цена снижена у товаров: {updated}.")

    @admin.action(description="Повысить цену выбранных товаров на 10%")
    def increase_price_10(self, request, queryset):
        updated = queryset.update(price=F("price") * Decimal("1.10"))
        self.message_user(request, f"Цена повышена у товаров: {updated}.")


admin.site.site_header = "Администрирование магазина"
admin.site.site_title = "Магазин"
admin.site.index_title = "Данные магазина"
