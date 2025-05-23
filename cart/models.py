from django.db import models
from users.models import customerUser
from products.models import Product, TimeStampedModel

# Create your models here.




class Cart(TimeStampedModel):
    user = models.ForeignKey(
        customerUser(), null=True, related_name="carts", on_delete=models.CASCADE
    )
    session_key = models.CharField(max_length=255)


class CartProduct(TimeStampedModel):
    cart = models.ForeignKey(
        Cart, related_name="cart_products", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="cart_products", on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=0)