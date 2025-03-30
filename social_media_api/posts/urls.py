from django.urls import path
from . import views


# "api/"
urlpatterns = [
    path("posts/", views.PostListAPIView.as_view(), name="list post"),
    path("post/create/", views.PostCreateAPIView.as_view(), name="create post"),
    path("my_posts/", views.MyPostListAPIView.as_view(), name="my posts"),
    path("my_post/retrieve/<int:pk>/", views.PostRetrieveUpdateDestroyAPIView.as_view(), name="my specific post retrieve"),
    path("my_post/update/<int:pk>/", views.PostRetrieveUpdateDestroyAPIView.as_view(), name="my specific post Update"),
    path("my_post/delete/<int:pk>/", views.PostRetrieveUpdateDestroyAPIView.as_view(), name="my specific post Delete"),
    path("post/<int:pk>/comments/", views.CommentOnlyListForPostAPIView.as_view(), name="comments for a post"),
    path("post/comment/<int:pk>/update/", views.CommentUpdateDeleteAPIView.as_view(), name="update a comment"),
    path("post/comment/<int:pk>/delete/", views.CommentUpdateDeleteAPIView.as_view(), name="delete a comment"),
    path("post/<int:pk>/comment/create/", views.CommentCreateAPIView.as_view(), name="create a comment"),
]