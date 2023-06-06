from django.urls import path,include
from . import views

urlpatterns = [
    path('userprofile/',views.userprofile,name='userprofile'),
    path('addaddress/',views.add_address,name='addaddress'),
    path('changepassword/',views.changepassword,name='changepassword'),
]    
