from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.PostListAPIView.as_view(), name="List Post")
]