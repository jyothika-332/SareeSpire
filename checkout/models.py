from django.db import models
from django.contrib.auth.models import AbstractUser,User
from checkout.models import *
from order.models import Order
from userprofile.models import UserAddress


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=50)
    discount = models.BigIntegerField(null=True)
    minimum_purchase = models.BigIntegerField(null=True)
    is_active = models.BooleanField(default=False)

class CouponUsed(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE, blank=True, null=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE, blank=True, null=True)