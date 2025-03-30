from django.urls import path
from . import views



urlpatterns = [
    # Posts endpoints
    path("posts/", views.PostListAPIView.as_view(), name="post-list"),
    path("posts/create/", views.PostCreateAPIView.as_view(), name="post-create"),
    path("posts/my/", views.MyPostListAPIView.as_view(), name="my-posts"),
    path("posts/<int:pk>/", views.PostRetrieveUpdateDestroyAPIView.as_view(), name="post-detail"),

    # Comments endpoints (nested under posts)
    path("posts/<int:post_pk>/comments/", views.CommentOnlyListForPostAPIView.as_view(), name="post-comments"),
    path("posts/my/comments/<int:pk>/", views.CommentUpdateDeleteAPIView.as_view(), name="comment-detail"),
    path("posts/<int:post_pk>/comments/create/", views.CommentCreateAPIView.as_view(), name="comment-create"),
    
]