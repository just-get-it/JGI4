from django.urls import path,include
from studio import views

urlpatterns = [
    path('', views.archbase, name="studio"),
    path('about/', views.about, name="studio"),
    path('services/', views.services, name="studio"),
    path('projects/', views.projects, name="studio"),
    path('gallery/', views.gallery, name="studio"),
    path('contact/', views.contact, name="studio"),
]