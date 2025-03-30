from django.shortcuts import render
from .serializers import PostReadSerializer, PostWriteSerializer, CommentSerializer
from .models import Post, Comment
from rest_framework import generics, permissions, mixins
from django.shortcuts import get_object_or_404



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

# create a comment for only the provided post
class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Get the post_pk from the URL kwargs.
        post_pk = self.kwargs.get('pk')
        # Retrieve the Post instance or return a 404 if not found.
        post = get_object_or_404(Post, pk=post_pk)
        # Save the comment with the given post and current user as the author.
        serializer.save(post=post, author=self.request.user)


# update/delete specific comments
class CommentUpdateDeleteAPIView(mixins.UpdateModelMixin, 
                                 mixins.DestroyModelMixin, 
                                 generics.GenericAPIView):
    queryset= Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(author=user)

    def put(self, request, *args, **kwargs):
        # Handle full update
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # Handle partial update
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Handle delete
        return self.destroy(request, *args, **kwargs)
    