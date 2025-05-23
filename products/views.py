from .models import Product, Category
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Count


# Create your views here.
def home(request):
    products = Product.objects.all()
    categories = Category.objects.annotate(product_count=Count("products"))
    images = [
        "banners/banner1.png",
        "banners/banner2.png",
    ]
    context = {"categories": categories, "products": products, "images": images}
    return render(request, "products/home.html", context)



def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)

    paginator = Paginator(products, 6)
    page = request.GET.get("page")
    paged_products = paginator.get_page(page)

    context = {
        "products": paged_products,
        "category": category,
    }
    return render(request, "products/category_products.html", context)


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    context = {
        "product": product,
        "rating_counts": 0,
        "rating_percentages": 0,
        "reviews": 0,
    }
    return render(request, "products/product-detail.html", context)