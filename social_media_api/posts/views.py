from rest_framework.permissions import SAFE_METHODS
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment
from rest_framework import viewsets, permissions


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