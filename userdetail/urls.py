"""movintrendz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import login_page,register_page,seller_register,buisness_register,profile,recover,brand_register, student_register, save_user_current_location
from .views import logout_page,staff_register,seller_dashboard,seller_info,staff_info,staff_profile, logistic_runner_register

from .views import show_other_staff,staff_profile_activity,create_production,csv_create_production
from .views import staff_profile_manager,staff_profile_orders,staff_notifications,show_other_seller
from seller_info.views import seller_label,seller_label_delete,seller_fit,seller_fit_delete,seller_season,seller_season_delete

from POM.views import measurements_form,measurement_delete,measurements,measurements_detail,measurements_compare
from POM.views import duplicate_measurements
from b2b.views import buisness_order


from .views import vendor_profile,vendor_notifications,vendor_profile_activity,vendor_profile_orders

from product.views import upload_product,vendor_product_upload,product_unit,service_unit
from .views import activities_order,activities_page,staffs_under_page,b2b_customer_staff,vendor_staff
from .views import orders_clubbed,orders_clubbed_filter,staff_profile_message,create_noti_staff,create_noti_vendor



from .views import vendor_profile_bom,vendor_profile_bom_details,vendor_custom_form,staff_profile_orders_list
from .views import create_production_products,staff_profile_allocate_garment,vendor_floated_orders


from .views import staff_profile_packing_list,staff_profile_distribution_list,staff_profile_cummlative

from .views import staff_profile_basic_order
from .views import vendor_activities_page,vendor_profile_vendors,vendor_profile_orders_list,logistic_request


from .views import quality_evaluation,vendor_profile_activity_by_id,staff_profile_products,staff_profile_product_detail
from .views import staff_profile_requested_product


from seller_info.views import seller_profile_notifications,seller_profile_b2b_customer,seller_profile_vendors,seller_profile_orders,seller_profile_products
from .document_views import qr_generate,qr_view,carton_details,carton_update_status,order_qr_scanner

from .views import staff_profile_placeorder,staff_profile_upload_product,staff_profile_holidays
from .vendor_views import vendor_new_order,update_availiable_products 
from .views import consumer_register,recover_otp,recover_password,vendor_profile_bom_ordering,vendor_trims_floated_orders

from seller_info.views import seller_profile_store,seller_yearly_budget
from .views import staff_address_details, trim_section_edit, manual_docs_edit,manual_docs_add
from .views import quality_evaluation_by_size,quality_evaluation_clubbed,washcare_detail_view,vendor_profile_compare_bom,vendor_profile_orders_lay,lay_detail_view1,lay_list,lay_detail_view2,lay_detail_view3,lay_detail_view4,lay_detail_view5
from .views import quality_evaluation_by_size,quality_evaluation_clubbed,washcare_detail_view,vendor_profile_compare_bom,vendor_profile_orders_cut,cut_list,cutting,staff_profile_orders_cut
from .views import login_other_profile,staff_profile_run_rate,staff_profile_status,alteration_assortment, manufacturer_register, new_seller_register

from seller_info.views import show_Layout
from product.views import service_unit,product_unit,add_subscription

urlpatterns = [
   path('save_user_current_location', save_user_current_location, name = "save_user_current_location" ),

   path('login/',login_page,name="login_page"),
   path('register/',register_page, name="register"),
   path('manufacturer_registration/', manufacturer_register, name="manufacturer_register"),
#    path('seller_registration/',seller_register, name="seller_register"),
   path('seller_registration/',new_seller_register, name="new_seller_register"),
   path('brand_registration/',brand_register),
   path('buisness_registration/',buisness_register, name="business_register"),
   path('student_registration/', student_register, name='student_register'),
   path('consumer_register',consumer_register, name="consumer_register"),
   path('profile/',profile),
   path('recover/',recover),
   path('recover/otp',recover_otp),
   path('recover/new_password/<str:key>',recover_password),
   path('logout/',logout_page, name="logout"),
   path('login_other_profile',login_other_profile),
   path('staff_registration/',staff_register, name="staff_register"),
   path('seller_profile/',seller_dashboard),
   path('seller_profile_update/',seller_info),
   path('seller_profile/label',seller_label),
   path('seller_profile/store',seller_profile_store, name='seller_profile_store'),
   path('seller_profile/label/<str:slug>',seller_label_delete),
   path('seller_profile/fit',seller_fit),
   path('seller_profile/product_unit',product_unit),
   path('seller_profile/add_subscription',add_subscription),
   path('seller_profile/service_unit',service_unit),
   path('seller_profile/fit/<str:slug>',seller_fit_delete),
   path('seller_profile/washcare/<int:washcare_id>',washcare_detail_view),
   path('seller_profile/trim_edit/<int:trim_section_id>', trim_section_edit, name='trim_edit'),
   path('seller_profile/manual_docs_edit/<int:manual_docs_id>', manual_docs_edit, name='manual_docs_edit'),
   path('seller_profile/manual_docs_order_add/<int:order_no>', manual_docs_add, name='manual_docs_order_add'),
   path('seller_profile/season',seller_season),
   path('seller_profile/season/<str:slug>',seller_season_delete),
   path('seller_profile/measurements_form/',measurements_form, name="measurement_form"),
   path('seller_profile/measurements/<str:slug>/delete',measurement_delete),
   path('seller_profile/measurements',measurements),
   path('seller_profile/measurements/compare',measurements_compare),
   path('seller_profile/measurements/<str:slug>',measurements_detail),
   path('seller_profile/duplicate_measurement/<str:slug>',duplicate_measurements),
   path('seller_profile/upload_product',upload_product,name='upload_product'),
   path('seller_profile/notifications',seller_profile_notifications),
   path('seller_profile/b2b_customer',seller_profile_b2b_customer),
   path('seller_profile/vendors',seller_profile_vendors),
   path('seller_profile/orders',seller_profile_orders),
   path('seller_profile/products',seller_profile_products),
   path('seller_profile/yearly_budget',seller_yearly_budget),
   path('seller_profile/<str:email>',show_other_seller),
   path('staff_profile_update/',staff_info),
   path('staff_profile/',staff_profile),
   path('save_extracted',views.save_extracted,name='save_extracted'),
   # sanskar
   path('seller_profile/show_layout_details/<int:layout_id>',show_Layout),
   path('staff_profile/notifications',staff_notifications),
   path('staff_profile/manager',staff_profile_manager),
   path('staff_profile/activities',activities_page),
   path('staff_profile/staffs',staffs_under_page),
   path('staff_profile/b2b_customer',b2b_customer_staff),
   path('staff_profile/vendors',vendor_staff),
   path('staff_profile/placeorder',staff_profile_placeorder),
   path('staff_profile/activities_order',activities_order),
   path('staff_profile/run-rate',staff_profile_run_rate),
   path('staff_profile/profile_status',staff_profile_status),
   path('staff_profile/profile_status/viewstatuses',views.staff_profile_status_view_statuses),
   path('staff_profile/activity/<str:activity_slug>', staff_profile_activity),
   path('staff_profile/orders/<int:order_no>/qr_generate/', qr_generate),
   path('staff_profile/orders/<int:order_no>/assortments/<str:email>', alteration_assortment),
   path('staff_profile/orders/<int:order_no>/scan_qr', order_qr_scanner),
   path('staff_profile/orders/<int:order_no>/qr_generate/view', qr_view),
   path('staff_profile/orders/<int:order_no>/qr_generate/carton/<int:carton_count>', carton_details),
   path('staff_profile/orders/<int:order_no>/update_status', carton_update_status),
   path('staff_profile/orders/<int:order_no>/forms/generate_carton_list', views.generate_carton_list),
   path('staff_profile/orders/<int:order_no>/forms/packing_list', views.show_carton_list),
   path('staff_profile/orders/<int:order_no>/generate_qr', views.generate_qr),
   path('staff_profile/orders/<int:order_no>/view_qr', views.view_qr),
   path('staff_profile/orders/<int:order_no>/inside_carton/<int:carton_no>', views.inside_carton),
   path('staff_profile/orders/<int:order_no>/print_individual_carton/<int:carton_no>', views.print_individual_carton),
   path('staff_profile/orders/view_all_qr/<int:order_no>', views.view_all_qr),
   path('staff_profile/orders/<int:order_no>/print_pieces_inside_carton/<int:carton_no>', views.print_all_pieces_qr),
   path('staff_profile/orders/print_pieces_in_individual_carton/<str:q>', views.print_pieces_in_individual_carton),
   path('staff_profile/orders/<int:order_no>/show_pieces_inside_carton/<int:carton_no>',
        views.show_pieces_in_individual),
   path('staff_profile/orders/<int:order_no>/forms/address_details', staff_address_details),
   path('staff_profile/orders/<int:order_no>/forms/distribution_list', staff_profile_distribution_list),
   path('staff_profile/orders/<int:order_no>/forms/cummlative', staff_profile_cummlative),
   path('staff_profile/orders/<int:order_no>/forms/logistic_request', logistic_request),
   path('staff_profile/orders/<int:order_no>/forms/quality_evaluation', quality_evaluation),
   path('staff_profile/orders/<int:order_no>/forms/quality_evaluation_clubbed', quality_evaluation_clubbed),
   path('staff_profile/orders/<int:order_no>/forms/quality_evaluation/<str:size_label>', quality_evaluation_by_size),
   path('staff_profile/orders/<int:order_no>', staff_profile_orders, name='staff_profile_orders'),
   path('staff_profile/orders/<int:order_no>/order_documents/', include('userdetail.documents_urls')),
   path('staff_profile/orders/<int:order_no>/allocate_garment', staff_profile_allocate_garment),
   path('staff_profile/production/<int:order_no>', create_production),
   path('staff_profile/csv_production/<int:order_no>', csv_create_production),
   path('staff_profile/packing/<int:order_no>', views.create_packinglist),
   path('staff_profile/show_packing/<int:order_no>', views.Packing_list),
   path('staff_profile/show_all_packing/<int:order_no>', views.ShowPacking),
   path('staff_profile/orders/<int:order_no>/<str:conc>', staff_profile_orders_cut,name="nav"),

   path('staff_profile/orders_clubbed',orders_clubbed),
   path('staff_profile/orders_clubbed_filter',orders_clubbed_filter),
   path('staff_profile/holidays',staff_profile_holidays),
   path('staff_profile/upload_product',staff_profile_upload_product),
   path('staff_profile/message',staff_profile_message),
   path('staff_profile/products',staff_profile_products),
   path('staff_profile/products/<str:slug>',staff_profile_product_detail),
   path('staff_profile/requested_product/<str:slug>/<int:id>',staff_profile_requested_product),
   path('staff_profile/create_noti_staff',create_noti_staff),
   path('staff_profile/create_noti_vendor',create_noti_vendor),
   path('staff_profile/orders',staff_profile_orders_list),
   path('staff_profile/<str:email>',show_other_staff),

   path('vendor_profile/',vendor_profile),
   path('vendor_profile/new_order',vendor_new_order),
   path('vendor_profile/create_production_products',create_production_products),
   path('vendor_profile/notifications',vendor_notifications),
   path('vendor_profile/activities',vendor_activities_page),
   path('vendor_profile/vendors',vendor_profile_vendors),
   path('vendor_profile/orders',vendor_profile_orders_list),
   path('vendor_profile/orderslay',lay_list,name='lay_list'),
   path('vendor_profile/cutting',cutting,name='cutting'),
   path('vendor_profile/orderscut',cut_list,name='cut_list'),
#    path('vendor_profile/inhouse',inhouse,name="inhouse"),                 #my funct--- akancha
   path('vendor_profile/floated_orders',vendor_profile_orders_list),
   path('vendor_profile/product_upload',vendor_product_upload),
   path('vendor_profile/update_availiable_products',update_availiable_products),
   path('vendor_profile/activity/<int:activity_slug>',vendor_profile_activity_by_id),
   path('vendor_profile/activity/<str:activity_slug>',vendor_profile_activity),
   path('vendor_profile/orders/<int:order_no>',vendor_profile_orders),
   path('vendor_profile/floated_orders/<int:order_no>',vendor_floated_orders),
   path('vendor_profile/orders/<int:order_no>/lay',vendor_profile_orders_lay,name='lay'),
   path('vendor_profile/orders/<int:order_no>/cut',vendor_profile_orders_cut,name='cut'),
   path('vendor_profile/orderslay/<int:order_no>/lay1/<str:color>',lay_detail_view1,name='detail1'),
   path('vendor_profile/orderslay/<int:order_no>/lay2/<str:color>',lay_detail_view2,name='detail2'),
   path('vendor_profile/orderslay/<int:order_no>/lay3/<str:color>',lay_detail_view3,name='detail3'),
   path('vendor_profile/orderslay/<int:order_no>/lay4/<str:color>',lay_detail_view4,name='detail4'),
   path('vendor_profile/orderslay/<int:order_no>/lay5/<str:color>',lay_detail_view5,name='detail5'),
   path('vendor_profile/trims_floated_orders/<int:trims_orders_no>',vendor_trims_floated_orders),
   path('vendor_profile/orders/<int:order_no>/forms/bom',vendor_profile_bom),
   path('vendor_profile/orders/<int:order_no>/forms/compare_bom',vendor_profile_compare_bom),
   path('vendor_profile/orders/<int:order_no>/forms/bom/<int:bom_id>',vendor_profile_bom_details),
   path('vendor_profile/orders/<int:order_no>/forms/bom/<int:bom_id>/ordering',vendor_profile_bom_ordering),
   path('vendor_profile/orders/<int:order_no>/forms/<int:form_id>',vendor_custom_form),
   # path('create_notification/staff'),
   #path('form/', views.showPage),
   path('staff_profile/orders/sizeassortment/', views.sizeAssortment),
   path('staff_profile/orders/new/<int:order_no>', views.ShowPage),
   path('staff_profile/orders/csv_update/new/<int:order_no>', views.UpdateCsv),
   path('staff_profile/orders/generate/', views.Forminput),
   path('staff_profile/orders/list/', views.GeneratePackingList),
   path('staff_profile/orders/viewlist/', views.PackingList),
   path('staff_profile/orders/carton_details/<int:carton>', views.Carton_details),
   path('academic_profile',views.academic_profile,name='academic_profile'),
   path('professional_profile',views.professional_profile,name='professional_profile'),
   path('social_profile',views.social_profile,name='social_profile'),
   path('medical_profile',views.medical_profile,name='medical_profile'), 
   path('product_order',views.product_order,name='product_order'), 
   path('services',views.services,name='services'), 
   path('order_product',views.order_product,name='order_product'),
   path('customize',views.customize,name='customize'), 
   path('seller_filter',views.seller_filter),
   path('final_product_order',views.final_product_order),
   path('service_order',views.service_order,name='service_order'), 
   path('order_service',views.order_service,name='order_service'), 
   path('final_service',views.final_service,name='final_service'), 
   path('seller_profile/service_unit',service_unit),
   path('customize',views.customize,name='customize'), 
   path('customize_service',views.customize_service,name='customize_service'),
   # subscription
   path('quickSubscribe', views.subscription, name='quick_subscribe'),
   path('subscription',views.newSubscription,name='subscription'),
   path('subscription/<str:slug>', views.productSubscribe, name='productSubscribe'),
   path('subscriptionSearch', views.subscriptionSearch, name="subscriptionSearch"),
   #path('finalsubscribe', views.subscriptionFinal, name='finalSubscribe'),
   #path('payForSubscription', views.payForSubscription, name='payForSubscription'),
   path('updateSubscription', views.updateSubscription, name='updateSubscription'),
   path('deleteSubscription', views.deleteSubscription, name='deleteSubscription'),
#    path('subscription_cart', views.subscriptionCart, name="subscriptionCart"),
   path('subPayWithWallet/<str:slug>', views.subPayWithWallet, name="subPayWithWallet"),
   path('subscriptionCheckout', views.subscriptionCheckout, name="subscriptionCheckout"),
   path('subscriptionPayment', views.subscriptionPayment, name="susbcriptionPayment"),
   #path('unit_quantity_filter',views.unit_quantity_filter,name='unit_quantity_filter'),
   #path('subscription_vendor_filter',views.subscription_vendor_filter,name='subscription_vendor_filter'),
   #path('final_subscription',views.final_subscription,name='final_subscription'),
   path('pick_and_deliver',views.pick_and_deliver,name='pick_and_deliver'),
   path('project_add',views.project_add,name="project_add"),
   path('skill_add',views.skill_add,name="skill_add"),
   path('certification_add',views.certification_add,name="certification_add"),
   path('add_address',views.add_address,name="add_address"),
   path('customer_rating_form/<int:order_no>', views.customer_rating_form,name="customer_rating_form"),
   path('delivery_rating_form/<int:order_no>', views.delivery_rating_form,name="delivery_rating_form"),
   path('seller_rating_form/<int:order_no>', views.seller_rating_form,name="seller_rating_form"),
   path('product_rating_form/<int:order_no>', views.product_rating_form,name="product_rating_form"),
   path('logistic_runner_registeration/',logistic_runner_register, name="logistic_runner_register"),
   path('add_distribution_center', views.add_distribution_center, name="add_distribution_center"),
   ]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
