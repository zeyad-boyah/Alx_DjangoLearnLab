from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment


User = get_user_model()

class CommentSerializer (serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    class Meta:
        model = Comment
        fields = ("author", "content","created_at","updated_at", "post")
        read_only_fields = ["author", "post"]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    comments = CommentSerializer(many=True)
    class Meta:
        model = Post
        fields = ("author","title", "content","created_at","updated_at", "comments")
        read_only_fields = ["author"]