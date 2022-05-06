



from django.contrib import admin
from django.urls import path,include


from .views import customadmin,productcategories,categorydetail
from .views import categorydelete,categoryadd
from .views import subcategories,subcategorydetail,subcategorydelete
from .views import subcategoryadd
from .views import productlist , productdetail,productdelete,productadd
from .views import supercategories , supercategoriesdetail,supercategoriesdelete,supercategoriesadd

app_name = 'customadmin'


urlpatterns = [
   path('',customadmin),
   path('productcategories/',productcategories,name='productcategories'),
   path('productcategories/<int:num>',categorydetail,name='categorydetail'),
   path('productcategories/<int:num>/delete',categorydelete,name='categorydelete'),
   path('productcategories/add',categoryadd,name='categoryadd'),
   path('subcategories/',subcategories,name='subcategories'),
   path('subcategories/<int:num>',subcategorydetail,name='subcategorydetail'),
   path('subcategories/<int:num>/delete',subcategorydelete,name='subcategorydelete'),
   path('subcategories/add',subcategoryadd,name='subcategoryadd'),

   path('product/',productlist,name='custom_product'),
   path('product/<str:id>',productdetail,name='custom_product_detail'),
   path('product/<str:id>/delete',productdelete,name='productdelete'),
   path('products/add',productadd,name='productadd'),

   path('supercategory/',supercategories,name='super-categories'),
   path('supercategory/<str:id>',supercategoriesdetail,name='custom_super_detail'),
   path('supercategory/<str:id>/delete',supercategoriesdelete,name='superdelete'),
   path('supercategoryy/add',supercategoriesadd,name='supercategoryadd'),
]
