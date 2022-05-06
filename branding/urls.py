from django.contrib import admin
from django.urls import path,include
from branding import views
from .views import port_app, videos, show_app, blog
from .views import content_writing, digital_marketing, digital_marketing_enquiry




urlpatterns = [
    path('',views.enquiry,name='branding'),
    path('portfolio/',views.portfolio, name='branding'),
    path('contact/',views.contact, name='branding'),
    path('about/',views.about, name='branding'),
    path('services/',views.services, name='branding'),
    path('user-experience/',views.user_experience, name='branding'),
    path('user-interface/',views.user_interface, name='branding'),
    path('explainer-video/',views.explainer_video, name='branding'),
    path('design-and-concept/',views.design_and_concept, name='branding'),
    path('social-media-marketing/',views.social_media_marketing, name='branding'),
    path('seo/',views.seo, name='branding'),
    path('animation/',views.animation, name='branding'),
    path('branding/',views.branding, name='branding'),
    path('presentation/',views.presentation, name='branding'),
    path('email-marketing/',views.email_marketing, name='branding'),
    path('content-strategy/',views.content_strategy, name='branding'),
    path('privacy-policy/',views.privacy_policy, name='branding'),
    path('termandcondition/',views.terms_and_conditions, name='branding'),
    path('industries/',views.industries, name='branding'),
    path('innovation/',views.innovation, name='branding'),
    path('blog/page/<int:num>',views.blogp, name='branding'),
    path('sourcing/', views.enquiry_sourcing),
    path('contact/', views.enquiry_contact),
    path('port_app/', port_app),
    path('show_appointment/', show_app),
    path('videos/', videos),
    path('blog/', blog),
    path('content-writing/', content_writing, name="content_writing"),
    path('digital-marketing/', digital_marketing, name="digital_marketing"),
    path('digital-marketing-enquiry/', digital_marketing_enquiry),
    # path('3D/', views.enquiry, name="enquiry_3D"),
]
