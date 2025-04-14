from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import ChatMessage, ChatGroup, TourChatMessage
from .serializers import ChatMessageSerializer, TourChatMessageSerializer
from group.models import Group
from tour.models import TourBooking


# چت خصوصی با گروه
class SendPrivateMessage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        chat_group, _ = ChatGroup.objects.get_or_create(group=group)

        message = ChatMessage.objects.create(
            chat_group=chat_group,
            sender=request.user,
            message=request.data.get('message')
        )
        serializer = ChatMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetPrivateMessages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        chat_group = get_object_or_404(ChatGroup, group=group)
        messages = ChatMessage.objects.filter(chat_group=chat_group).order_by('timestamp')
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)


# چت عمومی تور
class SendTourChatMessage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, tour_id):
        if not TourBooking.objects.filter(tour_id=tour_id, user=request.user).exists():
            return Response({"error": "You are not registered for this tour."}, status=403)

        message = TourChatMessage.objects.create(
            tour_id=tour_id,
            sender=request.user,
            message=request.data.get("message")
        )
        serializer = TourChatMessageSerializer(message)
        return Response(serializer.data, status=201)


class TourChatMessageList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tour_id):
        if not TourBooking.objects.filter(tour_id=tour_id, user=request.user).exists():
            return Response({"error": "You are not registered for this tour."}, status=403)

        messages = TourChatMessage.objects.filter(tour_id=tour_id).order_by('timestamp')
        serializer = TourChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
