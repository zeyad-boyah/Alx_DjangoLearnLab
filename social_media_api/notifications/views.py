from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer
from django.contrib.contenttypes.models import ContentType


# list notifications for user by how recent they are
class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retrieve notifications for the authenticated user
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')


class MarkNotificationAsReadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
        notification.read = True
        notification.save()
        return Response({"detail": "Notification marked as read."}, status=status.HTTP_200_OK)
    

def create_like_notification(actor, post):
    """
    Create a notification when a post is liked.
    """
    Notification.objects.create(
        recipient=post.author,
        actor=actor,
        verb="liked your post",
        target_content_type=ContentType.objects.get_for_model(post),
        target_object_id=post.pk
    )

def create_comment_notification(actor, post):
    """
    Create a notification when a post receives a comment.
    """
    Notification.objects.create(
        recipient=post.author,
        actor=actor,
        verb="commented on your post",
        target_content_type=ContentType.objects.get_for_model(post),
        target_object_id=post.pk
    )

def create_follower_notification(actor, user):
    """
    Create a notification when a user starts following another user.
    """
    Notification.objects.create(
        recipient=user,
        actor=actor,
        verb="started following you",
        target_content_type=ContentType.objects.get_for_model(user),
        target_object_id=user.pk
    )