from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import index, about, blog_details, blog, contact, elements, portfolio, pricing, kudugudu_contact

urlpatterns = [
    path('', index),
    path('about/', about),
    path('blog_details/', blog_details),
    path('blog/', blog),
    path('contact/', contact),
    path('elements/', elements),
    path('portfolio/', portfolio),
    path('pricing/', pricing),
    path('kudugudu-contact/', kudugudu_contact),
]