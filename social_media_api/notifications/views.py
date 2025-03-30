from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer


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