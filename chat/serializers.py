from rest_framework import serializers
from .models import ChatMessage, TourChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'chat_group', 'sender', 'sender_name', 'message', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'sender_name']


class TourChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = TourChatMessage
        fields = ['id', 'tour', 'sender', 'sender_name', 'message', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'sender_name']
