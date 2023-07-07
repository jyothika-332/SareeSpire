from django.urls import path,include
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    path('usertable/',views.usertable,name='usertable'),
    path('adminproduct/',views.adminproduct,name='adminproduct'),
    path('addproduct/',views.addproduct,name='addproduct'),
    path('report/',views.report,name='report'),
    path('sales_report_excel/',views.sales_report_excel,name='sales_report_excel'),
    path('deleteproduct/<int:prod_id>',views.deleteproduct,name='deleteproduct'),
    path('editproduct/<int:prod_id>',views.editproduct,name='editproduct'),
    path('block_user/<int:user_id>',views.block_user,name='block_user'),
] 