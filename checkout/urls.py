from django.urls import path,include
from . import views

urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path('placeorder/',views.place_order,name='placeorder'),
    path('proceed-to-pay/',views.razorpaycheck,name='proceed-to-pay'),
    path('confirmation/',views.confirmation,name='confirmation'),
    path('checkout_add_address/',views.checkout_add_address,name='checkout_add_address'),
    path('apply_coupon/',views.apply_coupon,name='apply_coupon'),
    path('admincoupon/',views.admincoupon,name='admincoupon'),
    path('addcoupon/',views.addcoupon,name='addcoupon'),
    path('editcoupon/<int:cpn_id>',views.editcoupon,name='editcoupon'),
    path('deletecoupon/<int:cpn_id>',views.deletecoupon,name='deletecoupon'),
]