from django.contrib import admin
from django.urls import path
from career.views import event

urlpatterns = [
    path('', event, name="career"),
]