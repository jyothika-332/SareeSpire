from django.urls import path,include
from . import views

urlpatterns = [
    path('admincategory/',views.admincategory,name='admincategory'),
    path('addcategory/',views.addcategory,name='addcategory'),
    path('adminvariation/',views.adminvariation,name='admin_variation'),
    path('add_variation/',views.add_variation,name='add_variation'),
    path('editvariation/<int:var_id>/',views.edit_variation,name='edit_variation'),
    path('deletevariation/<int:var_id>/',views.delete_variation,name='delete_variation'),
    path('editcategory/<int:cat_id>',views.editcategory,name='editcategory'),
    path('deletecategory/<int:cat_id>',views.deletecategory,name='deletecategory'),
] 