from django.urls import path,include
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    path('usertable/',views.usertable,name='usertable'),
    path('adminproduct/',views.adminproduct,name='adminproduct'),
    path('addproduct/',views.addproduct,name='addproduct'),
    # path('dwd_salesreport/',views.dwd_salesreport,name='dwd_salesreport'),
    path('deleteproduct/<int:prod_id>',views.deleteproduct,name='deleteproduct'),
    path('editproduct/<int:prod_id>',views.editproduct,name='editproduct'),
    path('block_user/<int:user_id>',views.block_user,name='block_user'),
] 