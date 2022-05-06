from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import about, retail_service, retail_product, fashion_product, experts, b2bsourcing, sourcing_pricing, tagDetail, \
    tags
from .views import new_user_sign_up, fashion_textile_service, fashion_apparel_service, fashion_hardgoods_service
from .views import fashion_design_service, contact,  quality_control, machine_maintenance 
from .views import product_planning, attendance_module, justgetit_admin,manufacturing

urlpatterns = [
    path('', about),

    #file upload
    path('tags/',tags),
    path('tag/<slug>',tagDetail,name='tag_detail'),

    path('retail-service/', retail_service),
    path('retail-product/', retail_product),
    path('fashion-product/', fashion_product),
    path('b2bsourcing/', b2bsourcing),
    path('sourcing-pricing/', sourcing_pricing),
    path('new-user-sign-up/', new_user_sign_up),
    path('fashion-textile-service/', fashion_textile_service),
    path('fashion-apparel-service/', fashion_apparel_service),
    path('fashion-hardgoods-service/', fashion_hardgoods_service),
    path('fashion-design-service/', fashion_design_service),
    path('contact/', contact),
    # path('about-contact/', about_contact),
    path('quality-control', quality_control, name="quality_control"),
    path('machine-maintenance', machine_maintenance, name="machine_maintenance"),
    path('product-planning', product_planning, name="product_planning"),
    path('attendance-module', attendance_module, name="attendance_module"),
    path('justgetit-admin/', justgetit_admin),
    path('manufacturing/', manufacturing),
    path('experts/', experts),
]