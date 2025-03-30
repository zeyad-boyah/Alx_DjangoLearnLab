from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.PostListAPIView.as_view(), name="list post"),
    path("post/create/", views.PostCreateAPIView.as_view(), name="create post"),
    path("my_posts/", views.MyPostListAPIView.as_view(), name="my posts"),
    path("my_post/retrieve/<int:pk>/", views.PostRetrieveUpdateDestroyAPIView.as_view(), name="my specific post retrieve"),
    path("my_post/update/<int:pk>/", views.PostRetrieveUpdateDestroyAPIView.as_view(), name="my specific post Update"),
    path("my_post/delete/<int:pk>/", views.PostRetrieveUpdateDestroyAPIView.as_view(), name="my specific post Delete"),
]