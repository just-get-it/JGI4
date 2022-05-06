




from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('',mydesign_home),
    path('profile/',mydesign_profile, name='mydesign_profile'),
    path('profile/<str:email>',mydesign_other_profile),
    path('notifications/',mydesign_notifications),
    path('messages/',mydesign_messages),
    path('newpost/',mydesign_newpost),
    path('editpost/<int:post_id>',mydesign_editpost, name='mydesign_editpost'),
    path('post/<int:post_id>', mydesign_post, name='mydesign_post'),
    path('interest/<str:interest_name>', mydesign_interest, name='mydesign_interest')
]
