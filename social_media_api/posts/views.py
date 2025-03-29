from django.shortcuts import render
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment
from rest_framework import generics 



class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer