from django.urls import path

from . import views



urlpatterns = [
    path("", views.home, name="home"),
    path("products/<slug:product_slug>", views.product_detail, name="product_detail"),
    path("categories/<slug:category_slug>/products",views.category_products, name="category_products"),
   
]
