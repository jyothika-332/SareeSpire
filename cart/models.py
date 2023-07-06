from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from product.models import ColorVariation
# from django.utils.text import slugify
# from django.urls import reverse

# Create your models here.

class Cart(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE,related_name='carts')
    is_paid = models.BooleanField(default=False)
    total_price = models.BigIntegerField(null=True)

    def __str__(self):
        return self.users.username


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    color = models.ForeignKey(ColorVariation,on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    price = models.BigIntegerField(null=True)

    def __str__(self):
        return self.product.product_name
    