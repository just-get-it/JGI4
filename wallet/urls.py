from django.contrib import admin
from django.urls import path,include

from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.wallet, name="wallet"),
    path('add/', views.addmoney, name="add_money"),
    path('send/', views.sendmoney),
    path('check_payment_status/', views.checkPaymentStatus, name="checkPayStatus"),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)