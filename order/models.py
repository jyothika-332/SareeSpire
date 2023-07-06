from django.db import models
from django.contrib.auth.models import AbstractUser,User
from product.models import Product, ColorVariation, Brand
from cart.models import Cart
from userprofile.models import UserAddress


# Create your models here.


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name_of_person = models.CharField(max_length=100,blank=True,null=True)
    phone = models.BigIntegerField(null=True)
    address = models.ForeignKey(UserAddress,on_delete=models.CASCADE,blank=True,null=True)
    total_amount = models.DecimalField(max_digits=50,decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    mode_of_payment = models.CharField(max_length=50,blank=True,null=True)



class Ordered_Product(models.Model):
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE,blank=True,null=True)
    product = models.ForeignKey(ColorVariation,on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.BigIntegerField(null=True)
    amount = models.DecimalField(max_digits=20,decimal_places=2)
    STATUS = (
        ('Order Confirmed','Order Confirmed'),
        ('Shipped','Shipped'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned'),
    ) 
    status = models.CharField(choices=STATUS,default='Order Confirmed')

    def __str__(self):
        return self.product.product


class Returned(models.Model):
    returned_product = models.ForeignKey(Ordered_Product,on_delete=models.CASCADE,blank=True,null=True)
    reason = models.CharField(max_length=50,blank=True,null=True)
    comments = models.CharField(max_length=350,blank=True,null=True)
