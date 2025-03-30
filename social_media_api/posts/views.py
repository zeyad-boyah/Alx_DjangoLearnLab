from rest_framework.permissions import SAFE_METHODS
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .models import Post, Comment, Like
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


# Custom permission: allow read-only access to everyone, but only allow editing/deleting if the user is the owner.
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow safe methods for any request.
        if request.method in SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the object.
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset for CRUD operations on posts.
    - List, retrieve, create, update, delete posts.
    - Only the owner can update or delete a post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the author to the current user on creation.
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset for CRUD operations on comments.
    - List, retrieve, create, update, delete comments.
    - Only the owner of the comment can update or delete it.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the author to the current user on creation.
        serializer.save(author=self.request.user)

'''
generate a feed based on the posts from users that the current user follows.
This view should return posts ordered by creation date, showing the most recent posts at the top.
'''
class UserFeed(generics.ListAPIView):
    serializer_class= PostSerializer
    permission_classes= [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get all users the current user is following.
        following_users = self.request.user.following.all()
        #  Return posts where the author is in the following list, ordered by creation date
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
    
class PostLikeAPIView(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # get primary key from slug
        post_pk = kwargs.get("pk")
        user = request.user
        # Retrieve the post instance using the primary key
        post_instance = get_object_or_404(Post, pk=post_pk) 
        # Check if the post is already liked by the user
        if Like.objects.filter(post=post_instance, user=user).exists():
            return Response(
                {"detail": "Post already liked."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create a new like
        Like.objects.create(post=post_instance, user=user)
        return Response(
            {"action": "Like", "post": post_instance.title},
            status=status.HTTP_201_CREATED
        )
    
class PostUnlikeAPIView(generics.GenericAPIView):
    queryset = Post.objects.all()
    
    # serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_pk = kwargs.get("pk")
        user = request.user
        post_instance = get_object_or_404(Post, pk=post_pk)
        
        # Check if a like exists for this user and post
        like_instance = Like.objects.filter(post=post_instance, user=user).first()
        if not like_instance:
            return Response(
                {"detail": "Post not liked."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete the like instance
        like_instance.delete()
        return Response(
            {"action": "Unlike", "post": post_instance.title},
            status=status.HTTP_200_OK
        )