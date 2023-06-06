from django.db import models

# Create your models here.

class Ads(models.Model):
    ad_name = models.CharField(max_length=100,null=False)
    image = models.FileField(blank=True,upload_to='photos/home')