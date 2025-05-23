from django.db import models

from django.utils.text import slugify


# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="categories")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()

    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    special_price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    unit = models.CharField(max_length=100, null=True, blank=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    category = models.ForeignKey(
        Category, null=True, related_name="products", on_delete=models.SET_NULL
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"Image for {self.product.name}"


