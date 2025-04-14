from django.db import models
from django.conf import settings
from group.models import Group
from tour.models import Tour  # اضافه کن بالا در imports
from django.contrib.auth import get_user_model


class ChatGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ChatMessage(models.Model):
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)



class TourChatMessage(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tour {self.tour.id} - {self.sender.username}: {self.message[:30]}"