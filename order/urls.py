from django.urls import path,include
from . import views

urlpatterns = [
    path('mainorderpage/',views.mainorderpage,name='mainorderpage'),
    path('order/<int:order_item_id>',views.order,name='order'),
    path('adminorder/',views.adminorder,name='adminorder'),
    path('adminsingleorder/<int:order_item_id>',views.adminsingleorder,name='adminsingleorder'),
    path('update-status/<int:order_item_id>',views.update_status,name='update_status'),
    path('cancel_order/<int:order_item_id>',views.cancel_order,name='cancel_order'),
    path('return_item/',views.return_item,name='return_item'),
] 

