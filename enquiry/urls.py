
from django.contrib import admin
from django.urls import path,include
from enquiry import views
from .views import port_app, enquiry, videos, enquiry_sourcing, show_app, enquiry_contact, blog
from .views import content_writing, digital_marketing, digital_marketing_enquiry


urlpatterns = [
    path('',views.enquiry,name='automation'),
    path('sourcing/', views.enquiry_sourcing),
    path('contact/', views.enquiry_contact),
    path('port_app/', port_app),
    path('show_appointment/', show_app),
    path('videos/', videos),
    path('blog/', blog),
    path('content-writing/', content_writing, name="content_writing"),
    path('digital-marketing/', digital_marketing, name="digital_marketing"),
    path('digital-marketing-enquiry/', digital_marketing_enquiry),
    path('3D/', views.enquiry, name="enquiry_3D"),
]
