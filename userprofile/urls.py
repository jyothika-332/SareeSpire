from django.urls import path,include
from . import views

urlpatterns = [
    path('userprofile/',views.userprofile,name='userprofile'),
    path('addaddress/',views.add_address,name='addaddress'),
    path('editaddress/<int:customer_id>',views.editaddress,name='editaddress'),
    path('editprofile/<int:user_id>',views.editprofile,name='editprofile'),
    path('deleteaddress/<int:adr_id>',views.deleteaddress,name='deleteaddress'),
    path('changepassword/',views.changepassword,name='changepassword'),
]    
