from django.contrib import admin
from django.urls import path,include
from academy import views
from .views import index



urlpatterns = [
    path('', index),
]