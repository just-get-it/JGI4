from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.index, name="phinix"),
    path('project/', views.project, name="phinix-project"),
    path('services/', views.services, name="phinix-services"),
    path('about/', views.about, name="phinix-about"),
    path('blog/', views.blog, name="phinix-blog"),
    path('single/', views.single, name="phinix-single"),
    path('contact/', views.contact, name="phinix-contact"),
]