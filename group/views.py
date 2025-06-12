# group/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Group, GroupMember, GroupImageGallery
from .serializers import GroupSerializer, GroupMemberSerializer, GroupImageGallerySerializer
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import IsGroupLeader
from rest_framework.permissions import AllowAny


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


#ادیت گروه توسط لیدر یا سازنده گروه
class GroupEdit(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        group = Group.objects.get(leader=request.user)
        serializer = GroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        group = Group.objects.get(leader=request.user)

        if not group:
            return Response({'detail': 'Group not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save(leader=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
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

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(leader=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

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
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        print("USER:", request.user)
        # گرفتن گروهی که user رهبرش هست
        try:
            group = Group.objects.get(leader=request.user)
        except Group.DoesNotExist:
            return Response({"detail": "گروهی یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        serializer = GroupImageGallerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(group=group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupGalleryListView(APIView):
    permission_classes = [AllowAny]  # یا IsAuthenticated اگر محدود باشه

    def get(self, request, group_id):
        images = GroupImageGallery.objects.filter(group_id=group_id).order_by('-uploaded_at')
        serializer = GroupImageGallerySerializer(images, many=True, context={'request': request})
        return Response(serializer.data)


class GroupGalleryUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsGroupLeader]

    def post(self, request, group_id):
        group = Group.objects.get(id=group_id)
        image = request.FILES.get('image')
        caption = request.data.get('caption', '')

        gallery_item = GroupImageGallery.objects.create(
            group=group,
            image=image,
            caption=caption
        )
        serializer = GroupImageGallerySerializer(gallery_item, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroupGalleryDeleteView(APIView):
    class GroupGalleryDeleteView(APIView):
        permission_classes = [IsAuthenticated, IsGroupLeader]

    def delete(self, request, group_id, image_id):
        try:
            image = GroupImageGallery.objects.get(id=image_id, group_id=group_id)
            image.delete()
            return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except GroupImageGallery.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
        