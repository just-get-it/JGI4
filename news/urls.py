from django.urls import path
from . import views


urlpatterns = [
    path('', views.NewsListView.as_view(), name="all_news"),
    path('create/', views.NewsCreateView.as_view(), name="create_news"),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name="detail_news"),
    path('news/<int:pk>/update/', views.NewsUpdateView.as_view(), name="update_news"),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name="delete_news"),


    path('postComment', views.newsComment, name="news_comment"),

    path('like/<int:pk>', views.likeView, name="news_like"),
    path('dislike/<int:pk>', views.dislikeView, name="news_dislike"),
]
