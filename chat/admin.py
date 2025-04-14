from django.contrib import admin
from .models import ChatGroup, ChatMessage, TourChatMessage



# Register your models here.
admin.site.register(ChatGroup)
admin.site.register(ChatMessage)
admin.site.register(TourChatMessage)
