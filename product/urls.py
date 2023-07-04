from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.productpage,name='product'),
    path('admin-offer/',views.adminoffer,name='adminoffer'),
    path('add-offer/',views.addoffer,name='addoffer'),
    path('edit-offer/<int:offer_id>/',views.editoffer,name='editoffer'),
    path('delete-offer/<int:offer_id>/',views.deleteoffer,name='deleteoffer'),
    path('<slug:category_slug>/',views.productpage,name='products_by_category'), 
    path('productdetails/<slug:category_slug>/<slug:product_slug>/',views.productdetails,name='product_details'),
    path('change-variant',views.change_variant,name='ChangeVariant'),
    path('product_search',views.product_search,name='product_search'),
] 