from django.urls import path,include
from archplan import views

urlpatterns = [
    path('', views.archbase, name="space"),
    path('about/', views.about, name="space"),
    path('services/', views.services, name="space"),
    path('projects/', views.projects, name="space"),
    path('gallery/', views.gallery, name="space"),
    path('contact/', views.contact, name="space"),
    path('blog/', views.blog, name="space"),
    path('<slug:slug>/', views.blog_detail, name="space"),
# urls copied from blogs/urls.py 
    # path('', views.PostListView.as_view(), name="all_posts"),
    path('create/', views.PostCreateView.as_view(), name="space"),
    # path('post/<int:pk>/', views.PostDetailView.as_view(), name="detail_post"),
    # path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name="update_post"),
    # path('post/<int:pk>/delete/',
    #      views.PostDeleteView.as_view(), name="delete   _post"),
    path('postComment', views.postComment, name="space"),
    # path('like/<int:pk>', views.likeView, name="like"),
    # path('dislike/<int:pk>', views.dislikeView, name="dislike"),
]
