from django.shortcuts import render
from .serializers import PostReadSerializer, PostWriteSerializer, CommentSerializer
from .models import Post, Comment
from rest_framework import generics, permissions
from django.contrib.auth.mixins import LoginRequiredMixin


# list all posts including their comments
class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostReadSerializer

# list all posts made by the authenticated user
class MyPostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)


# create a Post with a login token
class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostWriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    # make it so that the author is the owner of the token
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# while authorized retrieve a post made by the user, update or delete them
class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostWriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)


