from django.contrib import admin





# Register your models here.
class Products_Admin(admin.ModelAdmin):
    list_display = ('prod_name', 'brand', 'color', 'size', 'occassion', 'ideal_for', 'descr', 'image', 'offers', 'coupon', 'stock', 'price',)
