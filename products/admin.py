from django.contrib import admin

# Register your models here.
from .models import Category, Product, ProductImage
from django.utils.html import format_html

admin.site.register([Category, ProductImage])


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                obj.image.url,
            )
        return "(No image)"

    readonly_fields = ("image_preview",)
    fields = ("image_preview", "image")
    verbose_name_plural = "Product Images"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]