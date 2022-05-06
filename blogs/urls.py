from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name="all_posts"),

    path('create/', views.PostCreateView.as_view(), name="create_post"),

    path('post/<int:pk>/', views.PostDetailView.as_view(), name="detail_post"),

    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name="update_post"),

    path('post/<int:pk>/delete/',
         views.PostDeleteView.as_view(), name="delete   _post"),

    path('postComment', views.postComment, name="post_comment"),

    path('like/<int:pk>', views.likeView, name="like"),
    path('dislike/<int:pk>', views.dislikeView, name="dislike"),

]
