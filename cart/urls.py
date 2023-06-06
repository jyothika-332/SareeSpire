from django.urls import path,include
from . import views

urlpatterns = [
    path('cart/',views.cart,name='cart'),
    path('add-to-cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
]   