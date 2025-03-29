from django.shortcuts import render
from .serializers import PostReadSerializer, PostWriteSerializer, CommentSerializer
from .models import Post, Comment
from rest_framework import generics, permissions
from django.contrib.auth.mixins import LoginRequiredMixin



class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostReadSerializer

class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostWriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)