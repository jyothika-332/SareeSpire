from django.urls import path,include
from . import views

urlpatterns = [
    path('wishlist/',views.wishlist,name='wishlist'),
    path('add-to-wishlist/<int:id>/',views.add_to_wishlist,name='add-to-wishlist'),
    path('deletewishlist/<int:id>/',views.wishlist_remove,name='deletewishlist'),
    path('add-to-cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
]