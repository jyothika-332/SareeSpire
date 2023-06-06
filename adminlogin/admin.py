from django.contrib import admin
from product.models import Product
from product.models import Categories, Brand
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('brand_name',)}

admin.site.register(Product,ProductAdmin)
admin.site.register(Categories,CategoryAdmin)
admin.site.register(Brand,BrandAdmin)

