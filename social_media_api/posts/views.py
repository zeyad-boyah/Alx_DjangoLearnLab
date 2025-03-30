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

    # make sure that the user can do all of this to his own posts only
    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)
    

# retrieve all comments for a post
class CommentOnlyListForPostAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class= CommentSerializer

    def get_queryset(self):
        post_pk = self.kwargs.get('pk')
        return Comment.objects.filter(post=post_pk)

