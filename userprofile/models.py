from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserAddress(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    housename = models.CharField(max_length=150,blank=False)
    city = models.CharField(max_length=50,blank=False)
    state = models.CharField(max_length=50,blank=False)
    country = models.CharField(max_length=50,blank=False)
    phone = models.BigIntegerField()
    pincode = models.IntegerField()
    is_active = models.BooleanField(default=True)

class User_Otp(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.BigIntegerField()   


        