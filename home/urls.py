from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.homepage,name='home'),
    path('admin_ads/',views.admin_ads,name='admin_ads'),
    path('add_ads/',views.add_ads,name='add_ads'),
    path('edit_ads/<int:ads_id>/',views.edit_ads,name='edit_ads'),
    path('delete_ads/<int:ads_id>/',views.delete_ads,name='delete_ads'),
]    