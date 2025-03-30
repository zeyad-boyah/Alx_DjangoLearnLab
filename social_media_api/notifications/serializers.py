from .models import Notification
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()  # or define a nested serializer for more details
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('id', 'actor', 'verb', 'target', 'timestamp', 'read')

    def get_target(self, obj):
        # Return a string or a serialized representation of the target if needed
        return str(obj.target) if obj.target else None