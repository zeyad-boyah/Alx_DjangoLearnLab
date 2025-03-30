from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment


User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "author", "content", "created_at", "updated_at", "post", "post_title")
        read_only_fields = ["author", "created_at", "post_title"]




class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ("id", "author", "title", "content", "created_at", "updated_at", "comments")
        read_only_fields = ["author", "created_at", "updated_at", "comments"]

