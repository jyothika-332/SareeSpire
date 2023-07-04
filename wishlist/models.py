from django.db import models
from django.contrib.auth.models import User
from product.models import Product,ColorVariation

# Create your models here.

class Wishlist(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE,related_name='wishlist')
    product = models.ForeignKey(ColorVariation,on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.users.username 
    