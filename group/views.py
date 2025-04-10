# group/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Group, GroupMember, GroupImageGallery
from .serializers import GroupSerializer, GroupMemberSerializer, GroupImageGallerySerializer
from django.shortcuts import get_object_or_404

# ایجاد گروه
class CreateGroup(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data['leader'] = request.user.id  # لیدر گروه باید کاربر باشد
        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# مشاهده لیست گروه‌ها
class GroupList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

# مشاهده جزئیات یک گروه خاص
class GroupDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data)

# مشاهده اعضای یک گروه خاص
class GroupMembersList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        group = get_object_or_404(Group, pk=group_id)
        members = GroupMember.objects.filter(group=group)
        serializer = GroupMemberSerializer(members, many=True)
        return Response(serializer.data)

# اضافه کردن عضو به گروه
class AddGroupMember(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id):
        group = get_object_or_404(Group, pk=group_id)
        user = request.user
        if GroupMember.objects.filter(group=group, user=user).exists():
            return Response({"message": "User already a member."}, status=status.HTTP_400_BAD_REQUEST)

        group_member = GroupMember(group=group, user=user, status="Member", role="Member")
        group_member.save()
        return Response({"message": "User added to group."}, status=status.HTTP_201_CREATED)

# اضافه کردن تصویر به گالری گروه
class AddGroupImage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id):
        group = get_object_or_404(Group, pk=group_id)
        image = request.FILES.get('image')
        caption = request.data.get('caption')

        if not image or not caption:
            return Response({"message": "Image and caption are required."}, status=status.HTTP_400_BAD_REQUEST)

        image_gallery = GroupImageGallery(group=group, image=image, caption=caption)
        image_gallery.save()
        serializer = GroupImageGallerySerializer(image_gallery)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Create your views here.
