from django.urls import path, include
from .views import PostViewSet, CommentViewSet, UserFeed
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', UserFeed.as_view(), name="user-feed" ),
    path('posts/<int:pk>/like/', )
]


""" TODO
Routing Configuration:
Add URL patterns in posts/urls.py for liking and unliking posts, such as /posts/<int:pk>/like/ and /posts/<int:pk>/unlike/.
"""