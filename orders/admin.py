from django.contrib import admin

# Register your models here.
from .models import Order, OrderProduct, Payment

admin.site.register((Order, OrderProduct, Payment))