from django.contrib import admin
from django.urls import path,include
from academy import views
from .views import index, about, blog, blog_details, contact, courses, elements, login, register, academy_enquiry



urlpatterns = [
    path('', index),
    path('about/', about),
    path('blog/', blog),
    path('blog-details/', blog_details),
    path('contact/', contact),
    path('courses/', courses),
    path('elements/', elements),
    path('login/', login),
    path('register/', register),
    path('academy-enquiry/', academy_enquiry),
]