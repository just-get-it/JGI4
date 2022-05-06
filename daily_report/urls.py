from django.contrib import admin
from django.urls import path
from daily_report import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index),
    path("save", views.save),
    path('upload/<int:no>', views.upload),
    path('upload2/<int:no>', views.upload2),
    path('delete', views.delete),
    path('delete2', views.delete2),
    path('display_report', views.display_report),
    path('generate',views.generate, name='report_link'),
    path('display_report_user',views.display_report_user, name='report_staff'),
    path('display_report_user/unrated', views.display_unrated_reports, name='unrated_reports'),
    # path('new_link',views.new_link),
    path('<slug:slug1>/<slug:slug2>',views.form),
]
