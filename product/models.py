from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Categories(models.Model):
    slug = models.CharField(max_length=150, null=False ,blank=False)
    product_name = models.CharField(blank=False,max_length=50)
    description = models.TextField()
    # categories = models.CharField(blank=True,max_length=50,null=True)
    image = models.FileField(blank=True,upload_to='photos/category')

    def __str__(self) :
        return self.product_name
    def save(self, *args, **kwargs):
        # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.product_name)
        super(Categories, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('products_by_category',args=[self.slug])        



class Brand(models.Model):
    brand_name = models.CharField(max_length=100, null=True)
    image = models.FileField(blank=True,upload_to='photos/brand')
    description = models.CharField(max_length=100)
    slug = models.CharField(max_length=150, null=False ,blank=False)

    
    def __str__(self):
        return self.brand_name
    def save(self, *args, **kwargs):
        # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.brand_name)
        super(Brand, self).save(*args, **kwargs)

class Offer(models.Model):
    name = models.CharField(max_length=30, unique=True)
    discount = models.BigIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class Product(models.Model):
    slug = models.CharField(max_length=150, null=False ,blank=False)
    product_name = models.CharField(blank=False,max_length=50)
    description = models.TextField()
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE )
    image = models.FileField(blank=True,upload_to='photos/products')
    price = models.IntegerField(blank=False,null=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)

    def get_offer_price(self):
        amount = self.price - (self.price * self.offer.discount /100)
        return amount

    def get_url(self):
        return reverse('product_details', args=[self.categories.slug,self.slug])

    def __str__(self):
        return self.product_name
    
    def save(self, *args, **kwargs):
        # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)


class ColorVariation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    color = models.CharField(max_length=30)
    quantity = models.IntegerField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.color

