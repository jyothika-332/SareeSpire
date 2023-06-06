from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.productpage,name='product'),
    path('<slug:category_slug>/',views.productpage,name='products_by_category'), 
    path('productdetails/<slug:category_slug>/<slug:product_slug>/',views.productdetails,name='product_details'),
    path('change-variant',views.change_variant,name='ChangeVariant')
] 