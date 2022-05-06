from django.urls import path
from capacityrevenue import views

urlpatterns =  [
    path('', views.capacity_n_revenue, name='capacity_n_revenue'),
]