from django.urls import path,include
from . import views

urlpatterns = [
    path('admincategory/',views.admincategory,name='admincategory'),
    path('addcategory/',views.addcategory,name='addcategory'),
    path('editcategory/<int:cat_id>',views.editcategory,name='editcategory'),
    path('deletecategory/<int:cat_id>',views.deletecategory,name='deletecategory'),
] 