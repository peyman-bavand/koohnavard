# group/serializers.py

from rest_framework import serializers
from .models import Group, GroupMember, GroupImageGallery
from django.contrib.auth import get_user_model

# Serializer برای مدل گروه
class GroupSerializer(serializers.ModelSerializer):
    leader = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'leader', 'created_at', 'updated_at']

# Serializer برای مدل اعضای گروه
class GroupMemberSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())

    class Meta:
        model = GroupMember
        fields = ['id', 'user', 'group', 'joined_at', 'status', 'role']

# Serializer برای مدل گالری تصاویر گروه
class GroupImageGallerySerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())

    class Meta:
        model = GroupImageGallery
        fields = ['id', 'group', 'image', 'caption', 'uploaded_at']
