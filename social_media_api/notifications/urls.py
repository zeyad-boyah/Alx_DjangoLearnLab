from django.urls import path
from .views import NotificationListAPIView, MarkNotificationAsReadAPIView


urlpatterns = [
    path('notifications/', NotificationListAPIView.as_view(), name="list-notification-by-latest"),
    path('notifications/<int:pk>/', MarkNotificationAsReadAPIView.as_view(), name="mark-notification-as-read"),

]