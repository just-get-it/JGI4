from django.contrib import admin
from django.urls import path,include
from .views import *
from newrentapp.views import rentCart, rent_select_address, my_rentals
from django.conf.urls import url
urlpatterns = [
#    path('',products),

    path('get_order_coords/<int:order_item_id>/', get_order_coords, name = "get_order_coords" ),
    path('get_live_location_coords/<int:order_item_id>/', get_live_location_coords, name = "get_live_location_coords" ),
    url(r'delete', coupon_delete, name='delete_coupon'),
    url(r'apply/(?P<coupon_code>\w+)$', coupon_apply, name='apply_coupon'),
    path('update/', updatecart),
    path('cart/', cart, name='newcart'),
    path('select_address/', select_address, name='selectaddress'),
    path('manage_addresses/', manage_addresses, name='manageaddresses'),
    path('edit_addresses/', edit_addresses, name='editaddresses'),
    path('my_orders/', my_orders, name='myorders'),
    path('track_order/<int:order_id>', track_order, name="track_order"),
    path('order/<int:order_id>', order, name='order'),
    path('order/<int:order_id>/add_item', add_item, name='add_items'),
    path('order/<int:order_id>/edit_order', edit_order, name='edit_order'),
    path('order/<int:order_id>/update_existing_order', update_existing_order, name='update_existing_order'),
    path('order/payment_status', payment_status, name='paymentstatus'),
    path('subscription_cart', subscriptionCart, name="subscriptionCart"),
    path('subscribe_select_address/', subscribe_select_address, name='subscribe_selectaddress'),
    path('my_subscriptions/', my_subscriptions, name='mysubscriptions'),
    path('my_subscription_bills/', subscriptionBills, name='my_subscription_bills'),
    path('subuscription/<int:sub_orderID>/edit', editSubOrder, name='edit_subscription'),
    path('my_calendar/', calendar_view, name='my_calendar'),
    path('rent_cart', rentCart, name="rentCart"),
    path('rent_select_address/', rent_select_address, name='rent_selectaddress'),
    path('my_rentals/', my_rentals, name='myrentals'),
    path('select_distribution_centers/<int:order_id>', select_distribution_centers, name='select_distribution_centers'),
    path('order_to_be_delivered', order_to_be_delivered, name='order_to_be_delivered')
    
]   