from django.contrib import admin

# Register your models here.

from .models import Cart, CartProduct

admin.site.register([Cart, CartProduct])