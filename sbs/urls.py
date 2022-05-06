from django.urls import path,re_path
from . import views
from .views import ( 
                    index,
                    add,
                    update,
                    delete,
                    i,
                    create,
                    pages,
                    page1,
                    liked
                    #index,video_watch_view,liked_video,dislike_video,subscriber_view,video_comment, 
                   )


urlpatterns=[
   path('page', pages, name="home1"),
   path('index', index, name="home"),
   path('accounts/profile/',index,name="home2"),    
   path("add", add, name="edit"),
   path("create", create, name="create"),
   path("pages", pages, name="pages"),
   path("posti/<int:id>", page1, name="posti"),
   path("page1/<int:id>/", page1, name="page1"),
   path("cmnt/<int:id>", page1, name="page1"),
   path("like/<int:id>/<int:paid>", liked, name="page1"),
   #path("add1", add1, name="edit"),
   path("edit/<int:pk>", views.update.as_view(), name="update"),
   path("delete/<int:id>/", delete, name="home3"),
   #path("updt/<int:pk>", views.update1.as_view(), name="updt1"),
   #path("delt/<int:id>", delete1, name="home31"),
   #path("dowl/<int:id>", dl, name="home21"),
   path("filter",views.filter,name="j"),
   path("filter2",views.filter2,name="j2")
]
