from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="actor_notifications")
    verb = models.TextField()
    
    # Fields for GenericForeignKey
    # This field stores a reference to the model (its type) of the target object.
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    # This field stores the ID of the target object. Together with target_content_type, it uniquely identifies the target.
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    # This is not an actual database field but a convenience property. It uses  two fields to dynamically access the related object.
    target = GenericForeignKey('target_content_type', 'target_object_id')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # To track if notification has been seen

    def __str__(self):
        return f"{self.actor.username} {self.verb} {self.recipient.username}"