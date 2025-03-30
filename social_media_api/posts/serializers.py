from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment


User = get_user_model()

class CommentSerializer (serializers.ModelSerializer):
    # StringRelatedField will use the __str__ of the model and in the case the str of user model is the username
    author = serializers.StringRelatedField()

    post_title = serializers.CharField(source='post.title', read_only=True)
    class Meta:
        model = Comment
        fields = ("author", "content","created_at","updated_at", "post", "post_title")
        read_only_fields = ["author", "post", "created_at"]


class PostReadSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    comments = CommentSerializer(many=True)
    class Meta:
        model = Post
        fields = ("author","title", "content","created_at","updated_at", "comments")
        read_only_fields = ["author"]

class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "content"]

