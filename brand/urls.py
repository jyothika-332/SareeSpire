from django.urls import path,include
from . import views

urlpatterns = [
    path('adminbrand/',views.adminbrand,name='adminbrand'),
    path('addbrand/',views.addbrand,name='addbrand'),
    path('editbrand/<int:brnd_id>',views.editbrand,name='editbrand'),
    path('deletebrand/<int:brnd_id>',views.deletebrand,name='deletebrand'),
]    